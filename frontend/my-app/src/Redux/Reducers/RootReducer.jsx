import { combineReducers } from 'redux';
import SeatReducers from './SeatReducers';


const RootReducer = combineReducers({
    seat: SeatReducers
});

export default RootReducer;