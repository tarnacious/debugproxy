import type { SelectedHeaderType } from 'types/headers';
import type { FlowType } from 'types/flow';

export type ResponseState = {
  loading_response: boolean,
  updating_response: boolean,
  selected_response_header: ?SelectedHeaderType,
  response_data: ?string
}

export default ResponseState;
