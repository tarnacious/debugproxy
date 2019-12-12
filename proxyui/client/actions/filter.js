/* @flow */

import type { DispatchFilterType } from 'types/actions/filter';

export function changeQuery(query: string): DispatchFilterType {
  return {
    type: "CHANGE_QUERY",
    query: query
  }
}
