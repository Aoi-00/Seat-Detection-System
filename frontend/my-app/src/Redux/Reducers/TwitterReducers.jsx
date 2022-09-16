const initState = {
    items: [],
};

const TwitterReducers = (state = initState, action) => {
    switch(action.type){
        case 'FETCH_POST':
            return{
                ...state,
                items: action.payload
            }
        default:
            return state;
    }
}
export default TwitterReducers;