/* @flow */

export function filter(state : FilterStateType = {
  query: ''
}, action: DispatchFilterType) {
  switch (action.type) {
    case "CHANGE_QUERY":
      return Object.assign({}, state, {
        query: _.clone(action.query)
      })
    default:
      return state
  }
}

export default filter;
