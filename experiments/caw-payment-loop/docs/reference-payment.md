> ## Documentation Index
> Fetch the complete documentation index at: https://cobo.com/products/agentic-wallet/manual/llms.txt
> Use this file to discover all available pages before exploring further.

# Create payment

> Signs and submits a payment on behalf of the specified wallet using either the x402 or MPP protocol.

**Protocol selection** (required `protocol` field in the request body):
- `x402`: provide the `x402_payment_required` challenge object received from the payee server.
- `mpp`: provide the `mpp_www_authenticate` challenge string and, optionally, an `mpp_session` token.

**Idempotency**: if you supply a `request_id`, the endpoint checks for a previously completed transaction with the same `request_id` for this wallet. When a match is found the original result is returned immediately (`idempotent: true`) together with the original response headers (`retry_headers`) so you can replay the HTTP payment call without re-signing.

The wallet must be active (non-archived) and your principal must hold the `WALLET_TRANSFER` permission for the target wallet.



## OpenAPI

````yaml post /api/v1/wallets/{wallet_uuid}/payment
openapi: 3.1.0
info:
  title: Cobo Agentic Wallet Service
  description: Unified wallet engine for human and agent principals
  version: 1.3.0
servers: []
security: []
paths:
  /api/v1/wallets/{wallet_uuid}/payment:
    post:
      tags:
        - Transactions
      summary: Create payment
      description: >-
        Signs and submits a payment on behalf of the specified wallet using
        either the x402 or MPP protocol.


        **Protocol selection** (required `protocol` field in the request body):

        - `x402`: provide the `x402_payment_required` challenge object received
        from the payee server.

        - `mpp`: provide the `mpp_www_authenticate` challenge string and,
        optionally, an `mpp_session` token.


        **Idempotency**: if you supply a `request_id`, the endpoint checks for a
        previously completed transaction with the same `request_id` for this
        wallet. When a match is found the original result is returned
        immediately (`idempotent: true`) together with the original response
        headers (`retry_headers`) so you can replay the HTTP payment call
        without re-signing.


        The wallet must be active (non-archived) and your principal must hold
        the `WALLET_TRANSFER` permission for the target wallet.
      operationId: payment
      parameters:
        - name: wallet_uuid
          in: path
          required: true
          schema:
            type: string
            format: uuid
            description: >-
              UUID of the wallet to sign and submit the payment from. Obtain
              this value from the wallet creation or list-wallets response. The
              wallet must be active (not archived).
            title: Wallet Uuid
          description: >-
            UUID of the wallet to sign and submit the payment from. Obtain this
            value from the wallet creation or list-wallets response. The wallet
            must be active (not archived).
        - name: X-API-Key
          in: header
          required: false
          schema:
            title: X-Api-Key
            type: string
            nullable: true
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PaymentCreate'
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/StandardResponse_PaymentResult_'
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WrappedValidationError'
components:
  schemas:
    PaymentCreate:
      properties:
        protocol:
          $ref: '#/components/schemas/PaymentProtocol'
          description: 'Payment protocol: ''x402'' or ''mpp'''
        request_id:
          title: Request Id
          description: Idempotency key
          type: string
          maxLength: 255
          nullable: true
        x402_payment_required:
          title: X402 Payment Required
          description: Base64-encoded JSON from Payment-Required header
          type: string
          nullable: true
        mpp_www_authenticate:
          title: Mpp Www Authenticate
          description: WWW-Authenticate header raw value
          type: string
          nullable: true
        mpp_session:
          $ref: '#/components/schemas/MppSessionParams'
          description: Session parameters for MPP session actions (open/voucher/close)
          nullable: true
      type: object
      required:
        - protocol
      title: PaymentCreate
      description: |-
        Unified payment request.

        Protocol-specific fields are prefixed with protocol name (x402_ / mpp_).
    StandardResponse_PaymentResult_:
      properties:
        success:
          type: boolean
          title: Success
          default: true
        result:
          $ref: '#/components/schemas/PaymentResult'
        suggestion:
          type: string
          title: Suggestion
          default: ''
        message:
          type: string
          title: Message
          default: ''
        meta:
          $ref: '#/components/schemas/PaginationMeta'
          nullable: true
      type: object
      required:
        - result
      title: StandardResponse[PaymentResult]
    WrappedValidationError:
      title: WrappedValidationError
      type: object
      required:
        - success
        - error
      properties:
        success:
          type: boolean
          const: false
          default: false
          title: Success
        error:
          type: object
          title: Error
          required:
            - detail
          properties:
            detail:
              type: array
              title: Detail
              items:
                $ref: '#/components/schemas/ValidationError'
    PaymentProtocol:
      type: string
      enum:
        - x402
        - mpp
      title: PaymentProtocol
      description: Supported payment protocols.
    MppSessionParams:
      properties:
        action:
          $ref: '#/components/schemas/MppSessionAction'
          description: >-
            Session action: 'open' | 'voucher' | 'close' | 'request_close' |
            'withdraw'
        salt:
          title: Salt
          description: Random salt for session open (hex string)
          type: string
          nullable: true
        deposit:
          title: Deposit
          description: Deposit amount for session open (raw token units)
          type: string
          nullable: true
        channel_id:
          title: Channel Id
          description: >-
            Payment channel identifier, required for voucher, close,
            request_close, and withdraw actions.
          type: string
          nullable: true
        cumulative_amount:
          title: Cumulative Amount
          description: >-
            Cumulative total amount paid so far in this channel, expressed in
            raw token units. Required for voucher actions.
          type: string
          nullable: true
        payer_address:
          title: Payer Address
          description: >-
            On-chain address of the payer who opened the payment channel.
            Required for voucher/close actions.
          type: string
          nullable: true
        challenge_cache:
          $ref: '#/components/schemas/MppChallenge'
          description: Cached challenge for voucher/close (no 402 re-negotiation)
          nullable: true
      type: object
      required:
        - action
      title: MppSessionParams
      description: >-
        Parameters for MPP session actions (open / voucher / close /
        request_close / withdraw).
    PaymentResult:
      properties:
        id:
          title: Id
          description: Unique identifier assigned to this payment record.
          type: string
          format: uuid
          nullable: true
        idempotent:
          type: boolean
          title: Idempotent
          description: >-
            True if this result was served from a cached response for a
            previously processed request_id; false if it was freshly processed.
          default: false
        request_id:
          title: Request Id
          description: Idempotency key echoed back from the original payment request.
          type: string
          nullable: true
        protocol:
          $ref: '#/components/schemas/PaymentProtocol'
          description: '''x402'' or ''mpp'''
        status:
          type: string
          title: Status
          description: completed / submitted / failed
        retry_headers:
          additionalProperties:
            type: string
          type: object
          title: Retry Headers
          description: >-
            Headers to set when retrying the original request. x402:
            {'PAYMENT-SIGNATURE': '...'}. MPP: {'Authorization': 'Payment
            <cred>'}.
        mpp_session_info:
          $ref: '#/components/schemas/MppSessionInfo'
          description: >-
            MPP session details populated only when the action is 'open'. Null
            for all other actions.
          nullable: true
        tx_hash:
          title: Tx Hash
          description: >-
            On-chain transaction hash returned for request_close and withdraw
            actions. Null for all other actions.
          type: string
          nullable: true
      type: object
      required:
        - protocol
        - status
      title: PaymentResult
      description: |-
        Unified payment result.

        CLI uses retry_headers to retry the original request.
    PaginationMeta:
      properties:
        total:
          title: Total
          type: integer
          nullable: true
        offset:
          title: Offset
          type: integer
          nullable: true
        limit:
          title: Limit
          type: integer
          nullable: true
        has_more:
          title: Has More
          type: boolean
          nullable: true
        after:
          title: After
          type: string
          nullable: true
        before:
          title: Before
          type: string
          nullable: true
      type: object
      title: PaginationMeta
      description: |-
        Pagination metadata for list responses.

        Supports both legacy offset-based and cursor-based pagination.
        Cursor fields (``has_more``, ``after``, ``before``) are populated for
        cursor-paginated endpoints.  Legacy fields (``offset``, ``limit``) are
        populated when the caller uses the deprecated ``offset`` parameter.
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
        input:
          title: Input
        ctx:
          type: object
          title: Context
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
    MppSessionAction:
      type: string
      enum:
        - open
        - voucher
        - close
        - request_close
        - withdraw
      title: MppSessionAction
      description: MPP session action types.
    MppChallenge:
      properties:
        id:
          type: string
          title: Id
        realm:
          type: string
          title: Realm
        method:
          type: string
          title: Method
        intent:
          type: string
          title: Intent
        request:
          additionalProperties: true
          type: object
          title: Request
        request_b64:
          type: string
          title: Request B64
        expires:
          type: string
          title: Expires
          default: ''
        description:
          type: string
          title: Description
          default: ''
      type: object
      required:
        - id
        - realm
        - method
        - intent
        - request
        - request_b64
      title: MppChallenge
      description: Parsed MPP Payment challenge from WWW-Authenticate header.
    MppSessionInfo:
      properties:
        payer_address:
          type: string
          title: Payer Address
          description: On-chain address of the payer who opened the payment channel.
        chain_id:
          type: string
          title: Chain Id
          description: >-
            Cobo chain ID on which the payment channel was opened (e.g. 'ETH'
            for Ethereum mainnet). Call the List supported chains operation (GET
            /metadata/chains) to retrieve all supported chain IDs.
        channel_id:
          title: Channel Id
          description: >-
            Unique identifier of the opened payment channel. May be absent if
            the channel is not yet confirmed on-chain.
          type: string
          nullable: true
      type: object
      required:
        - payer_address
        - chain_id
      title: MppSessionInfo
      description: >-
        MPP session details returned by the backend after a successful channel
        open action.

````