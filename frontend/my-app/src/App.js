import logo from './logo.svg';
import { Route, Routes } from 'react-router-dom'; //use Link to not a href, useMatch end:true for absolute, useResolvedPath (absolute path if /pricing, relative if pricing)
import Home from './pages/Home'
import Store from './Redux/Store/Store'
import { Provider } from 'react-redux';

function App() {
  return (
    <Provider store={Store}>
      <div className="pt-3 p-0 m-0">
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </div>
    </Provider>
  );
}

export default App;
