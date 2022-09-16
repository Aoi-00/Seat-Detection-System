import { combineReducers } from 'redux';
import TwitterReducers from './TwitterReducers'
import SeatReducers from './SeatReducers';


const RootReducer = combineReducers({
    twitter: TwitterReducers,
    seat: SeatReducers
});

export default RootReducer;