import 'styles/main.scss';

import React from 'react';
import { render } from 'react-dom';
import Root from './Root';
import { AppContainer } from 'react-hot-loader';
import Redbox from 'redbox-react';

import configureStore from 'configureStore'
const store = configureStore();

const consoleErrorReporter = ({error}) => {
  console.error(error);
  return <Redbox error={error} />;
};

consoleErrorReporter.propTypes = {
  error: React.PropTypes.instanceOf(Error).isRequired
};

const renderRoot = Component => {
  render(
    <AppContainer errorReporter={consoleErrorReporter}>
      <Component store={ store } />
    </AppContainer>,
    document.getElementById('js-main')
  )
}

renderRoot(Root);

if (module.hot) {
  module.hot.accept('./Root', () => {
    renderRoot(Root);
  });
}
