import { createStore, applyMiddleware, compose } from 'redux';
import thunk from 'redux-thunk';
import RootReducer from '../Reducers/RootReducer'
//redux dev tools for development purposes
const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const initialState = {};
const middleWare = [thunk];
const store = createStore(
    RootReducer,
    initialState,
    composeEnhancers(
        applyMiddleware(...middleWare)
    )
);

export default store;