import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './Login';
import LobbyList from './LobbyList';
import Lobby from './Lobby'; // Import the Lobby component

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/lobbies" element={<LobbyList />} />
                <Route path="/lobby" element={<Lobby />} /> {/* Add the Lobby route */}
            </Routes>
        </Router>
    );
};

export default App;