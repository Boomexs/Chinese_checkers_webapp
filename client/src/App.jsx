import React, { useState } from 'react'
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom'
import { io } from 'socket.io-client'

const Login = () => {
    const [username, setUsername] = useState('')
    const [socket, setSocket] = useState('')
    const navigate = useNavigate()

    const handleUsername = (event) => {
        setUsername(event.target.value)
    }

    const handleSocket = (event) => {
        setSocket(event.target.value)
    }

    const connect = () => {
        const socketConnection = io('http://localhost:' + socket)

        socketConnection.on('connect', () => {
            console.log('Connected to server')
            navigate('/dashboard')
        })

        socketConnection.on('show_options', (data) => {
            console.log('Options:', data.options)
        })

        socketConnection.on('message', (message) => {
            console.log('Message:', message)
        })
    }

    return (
        <>
            <h1>Log in</h1>
            <div style={{ marginBottom: '20px' }}>
                <label>
                    User name: {''}
                    <input value={username} onChange={handleUsername} />
                </label>
            </div>
            <div style={{ marginBottom: '20px' }}>
                <label>
                    Socket: {''}
                    <input value={socket} onChange={handleSocket} />
                </label>
            </div>
            <button onClick={connect}>Connect</button>
        </>
    )
}

const Dashboard = () => {
    return (
        <div>
            <h1>Dashboard</h1>
            <p>Welcome to the dashboard!</p>
        </div>
    )
}

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/dashboard" element={<Dashboard />} />
            </Routes>
        </Router>
    )
}

export default App