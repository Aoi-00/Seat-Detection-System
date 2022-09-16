const initState = {
  libary: [],
  data: []
};

const SeatReducers = (state = initState, action) => {
  switch (action.type) {
    case "FETCH_LIB":
      return {
        ...state,
        library: action.payload,
      };
    case "FETCH_DATA":
      return {
        ...state,
        data: action.payload,
      };
    default:
      return state;
  }
};
export default SeatReducers;
