export const fetchLib = () => dispatch => {
    fetch('https://vast-basin-00497.herokuapp.com/https://libapp.ntu.edu.sg/NTULibraryGoWhere/Update')
        .then(res => res.json())
        .then(data => dispatch({
            type: 'FETCH_LIB',
            payload: data
        })
        );
}

export const fetchData = () => dispatch => {
    fetch('http://localhost:5000/')
        .then(res => res.json())
        .then(data => dispatch({
            type: 'FETCH_DATA',
            payload: data
        })
        );
}