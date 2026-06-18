/**
 * Step 2 — CLIENT coordinates and delegates via A2A (@a2a-js/sdk client)
 *
 * 1. ClientFactory resolves DEV's AgentCard from /.well-known/agent-card.json
 * 2. CLIENT sends task "Write a hello world script in Python"
 *    Message.metadata carries: client_agent_id, dev_agent_id, task_id, client_address
 * 3. Returns the completed Task (which contains the EAS-attested artifact from Step 3)
 */

import { v4 as uuidv4 } from 'uuid';
import { ClientFactory } from '@a2a-js/sdk/client';
import type { MessageSendParams, Task, DataPart, TextPart } from '@a2a-js/sdk';
import { DEV_SERVER_URL, CLIENT_ADDRESS, log } from './config.js';
import { saveState } from './state.js';

export interface DeliverableData {
  deliverable_hash: string;
  eas_attestation_uid: string;
  eas_schema_uid: string;
}

export interface DelegateTaskResult {
  task: Task;
  taskId: string;
  contextId: string;
  artifactData: DeliverableData;
  deliverableContent: string;
}

export async function delegateTask(
  clientAgentId: bigint,
  devAgentId: bigint,
): Promise<DelegateTaskResult> {
  log('STEP 2', '=== CLIENT delegating task to DEV via A2A ===');

  // SDK auto-resolves agent card and discovers the JSON-RPC endpoint
  const factory = new ClientFactory();
  const client = await factory.createFromUrl(DEV_SERVER_URL);
  log('STEP 2', `Agent card resolved from ${DEV_SERVER_URL}`);

  const taskId = uuidv4();

  const params: MessageSendParams = {
    message: {
      kind: 'message',
      messageId: uuidv4(),
      role: 'user',
      parts: [{ kind: 'text', text: 'Write a hello world script in Python.' }],
      // Metadata links A2A task to ERC-8004 agent IDs and EAS attestation
      metadata: {
        client_agent_id: clientAgentId.toString(),
        dev_agent_id: devAgentId.toString(),
        task_id: taskId,
        client_address: CLIENT_ADDRESS,
      },
    },
  };

  log('STEP 2', `Sending A2A task: taskId=${taskId}`);
  log('STEP 2', `  client_agent_id=${clientAgentId}  dev_agent_id=${devAgentId}`);

  const result = await client.sendMessage(params);

  if (result.kind !== 'task') {
    throw new Error(`Expected task response, got: ${result.kind}`);
  }

  const task = result as Task;
  log('STEP 2', `Task received: status=${task.status.state}`);

  if (!task.artifacts?.length) {
    throw new Error('Task completed but no artifacts returned');
  }

  const artifact = task.artifacts[0];
  const deliverableContent = artifact.parts
    .filter((p): p is TextPart => p.kind === 'text')
    .map((p) => p.text)
    .join('');

  const dataPart = artifact.parts.find((p): p is DataPart => p.kind === 'data');
  if (!dataPart) throw new Error('Artifact missing data part with EAS info');
  const artifactData = dataPart.data as unknown as DeliverableData;

  log('STEP 2', `Artifact received:`);
  log('STEP 2', `  deliverable_hash:     ${artifactData.deliverable_hash}`);
  log('STEP 2', `  eas_attestation_uid:  ${artifactData.eas_attestation_uid}`);
  log('STEP 2', `  eas_schema_uid:       ${artifactData.eas_schema_uid}`);

  saveState({ a2aTaskId: taskId, a2aContextId: task.contextId });

  return { task, taskId, contextId: task.contextId, artifactData, deliverableContent };
}
