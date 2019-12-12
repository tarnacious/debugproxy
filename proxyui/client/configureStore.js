import { createStore, applyMiddleware } from 'redux'
import thunkMiddleware from 'redux-thunk'
import rootReducer from 'reducers/root'
import createLogger from 'redux-logger'

export default function configureStore(initialState : any) {

  // Socket needs to be removed from global state
  //require('redux-immutable-state-invariant').default()
  let middleware = [ thunkMiddleware ];

  if (process.env.NODE_ENV !== 'production') {
    let logger = createLogger();
    middleware = [...middleware, logger];
  }

  const store = createStore(
    rootReducer,
    initialState,
    applyMiddleware(...middleware)
  )

  if (module.hot) {
    module.hot.accept('./reducers/root', () => {
      const nextRootReducer = require('./reducers/root').default;
      store.replaceReducer(nextRootReducer);
    });
  }

  return store;
}
