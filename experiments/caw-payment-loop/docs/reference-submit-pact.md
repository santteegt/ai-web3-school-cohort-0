> ## Documentation Index
> Fetch the complete documentation index at: https://cobo.com/products/agentic-wallet/manual/llms.txt
> Use this file to discover all available pages before exploring further.

# Submit pact for approval

> Submit a pact specification for human approval. Your agent's identity is resolved from the authenticated API key. The pact enters `PENDING_APPROVAL` status and a notification is sent to the Cobo Agentic Wallet app. For unpaired agents, the pact is auto-approved and enters `ACTIVE` status immediately.



## OpenAPI

````yaml post /api/v1/pacts/submit
openapi: 3.1.0
info:
  title: Cobo Agentic Wallet Service
  description: Unified wallet engine for human and agent principals
  version: 1.3.0
servers: []
security: []
paths:
  /api/v1/pacts/submit:
    post:
      tags:
        - Pacts
      summary: Submit pact for approval
      description: >-
        Submit a pact specification for human approval. Your agent's identity is
        resolved from the authenticated API key. The pact enters
        `PENDING_APPROVAL` status and a notification is sent to the Cobo Agentic
        Wallet app. For unpaired agents, the pact is auto-approved and enters
        `ACTIVE` status immediately.
      operationId: submit_pact
      parameters:
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
              $ref: '#/components/schemas/PactSubmitRequest'
      responses:
        '200':
          description: Already exists (idempotent). Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/StandardResponse_PactSubmitResponse_'
        '201':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/StandardResponse_PactSubmitResponse_'
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WrappedValidationError'
components:
  schemas:
    PactSubmitRequest:
      properties:
        wallet_id:
          type: string
          format: uuid
          title: Wallet Id
          description: Target wallet UUID.
        intent:
          type: string
          maxLength: 2000
          minLength: 1
          title: Intent
          description: Natural language description of the task.
        original_intent:
          title: Original Intent
          description: >-
            Raw user input that originated this pact request. For multi-turn
            conversations, messages are concatenated.
          type: string
          nullable: true
        spec:
          $ref: '#/components/schemas/PactSpec-Input'
          description: The pact specification.
        name:
          title: Name
          description: Human-readable pact name. Derived from intent if absent.
          type: string
          maxLength: 255
          minLength: 1
          nullable: true
        recipe_slugs:
          title: Recipe Slugs
          description: >-
            Slugs of recipes (from the recipes table) to associate with this
            pact.
          items:
            type: string
          type: array
          nullable: true
      type: object
      required:
        - wallet_id
        - intent
        - spec
      title: PactSubmitRequest
      description: Request body for POST /pacts/submit.
    StandardResponse_PactSubmitResponse_:
      properties:
        success:
          type: boolean
          title: Success
          default: true
        result:
          $ref: '#/components/schemas/PactSubmitResponse'
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
      title: StandardResponse[PactSubmitResponse]
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
    PactSpec-Input:
      properties:
        policies:
          items:
            $ref: '#/components/schemas/InlinePolicyCreate'
          type: array
          title: Policies
          description: Policy rules constraining the operator's actions.
        completion_conditions:
          items:
            $ref: '#/components/schemas/CompletionCondition'
          type: array
          title: Completion Conditions
          description: >-
            Conditions that trigger automatic pact completion (any-of
            semantics).
        execution_plan:
          title: Execution Plan
          description: >-
            Free-form execution plan derived from the intent, in markdown
            format. Presented to the owner during approval review so they can
            understand exactly what the operator will do. Suggested sections: #
            Summary, # Contract Operations, # Risk Controls, # Schedule.
          type: string
          nullable: true
      type: object
      title: PactSpec
      description: >-
        The core pact specification — defines policies and completion
        conditions.
    PactSubmitResponse:
      properties:
        pact_id:
          type: string
          format: uuid
          title: Pact Id
          description: Unique identifier for the pact.
        status:
          $ref: '#/components/schemas/PactStatus'
          description: Pact status.
        approval_id:
          type: string
          format: uuid
          title: Approval Id
          description: >-
            ID of the approval record created for this pact. Use this to track
            or action the approval workflow.
        message:
          type: string
          title: Message
          description: Human-readable status message.
      type: object
      required:
        - pact_id
        - status
        - approval_id
        - message
      title: PactSubmitResponse
      description: Response for POST /pacts/submit.
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
    InlinePolicyCreate:
      properties:
        name:
          type: string
          maxLength: 255
          minLength: 1
          title: Name
        type:
          $ref: '#/components/schemas/PolicyType'
          description: >-
            Policy category. Possible values: `transfer`, `contract_call`,
            `message_sign`.
        rules:
          additionalProperties: true
          type: object
          title: Rules
          description: >-
            Policy rule configuration. Structure depends on `type`; see the
            policy rules schema for each type.
        priority:
          type: integer
          title: Priority
          description: >-
            Evaluation priority. Higher values take precedence when multiple
            policies match.
          default: 0
        is_active:
          type: boolean
          title: Is Active
          description: 'Whether this policy is active. `true`: enforced. `false`: disabled.'
          default: true
      type: object
      required:
        - name
        - type
      title: InlinePolicyCreate
      description: Inline policy payload used during delegation/pact create.
    CompletionCondition:
      properties:
        type:
          $ref: '#/components/schemas/CompletionConditionType'
          description: >-
            Condition type. Possible values: `time_elapsed` (seconds since
            activation), `tx_count` (transaction count), `amount_spent` (token
            amount), `amount_spent_usd` (USD value), `manual` (no automatic
            trigger).
        threshold:
          title: Threshold
          description: >-
            Threshold value that triggers completion. Required for all types
            except `manual`. Format varies by type: integer string for
            `tx_count`, decimal string for amounts, integer seconds for
            `time_elapsed`.
          type: string
          nullable: true
      type: object
      required:
        - type
      title: CompletionCondition
      description: A single completion condition within PactSpec.
    PactStatus:
      type: string
      enum:
        - pending_approval
        - active
        - rejected
        - completed
        - expired
        - revoked
        - withdrawn
      title: PactStatus
      description: Pact lifecycle states.
    PolicyType:
      type: string
      enum:
        - transfer
        - contract_call
        - message_sign
      title: PolicyType
      description: |-
        Supported policy categories.

        Subset of ``caw_types.transaction.UserTransactionOperationType`` —
        values are shared so UT operation_type strings can be compared directly
        against PolicyType. Deposit is excluded because deposits are not
        policy-gated.
    CompletionConditionType:
      type: string
      enum:
        - time_elapsed
        - tx_count
        - amount_spent
        - amount_spent_usd
        - manual
      title: CompletionConditionType
      description: Supported pact completion condition types.

````