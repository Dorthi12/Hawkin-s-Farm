import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import "./index.css";

// Import Pages
import Login from './pages/Auth/Login.js';
import Signup from './pages/Auth/Signup.js';
// Placeholder pages (You'll develop these next)
const Marketplace = () => <h1 className="text-white p-8 bg-gray-900 min-h-screen">Welcome to the Marketplace!</h1>; 
const FarmerDashboard = () => <h1 className="text-white p-8 bg-gray-900 min-h-screen">Farmer Dashboard</h1>;

function App() {
    const handleLogin = (role) => {
        // Redirect logic handled here
        if (role === 'Farmer') {
            window.location.href = '/farmer/dashboard';
        } else {
            window.location.href = '/marketplace';
        }
    };

    const handleSignup = () => {
        // Redirect to login after successful signup
        window.location.href = '/login';
    };

    return (
        <Router>
            <Routes>
                {/* Public Auth Routes */}
                <Route path="/" element={<Login onSuccessfulLogin={handleLogin} />} />
                <Route path="/login" element={<Login onSuccessfulLogin={handleLogin} />} />
                <Route path="/signup" element={<Signup onSuccessfulSignup={handleSignup} />} />
                
                {/* Protected Routes (Needs role check in a real app) */}
                <Route path="/marketplace" element={<Marketplace />} />
                <Route path="/farmer/dashboard" element={<FarmerDashboard />} />

                {/* Fallback */}
                <Route path="*" element={<h1 className="text-white p-8 bg-gray-900 min-h-screen">404 Not Found</h1>} />
            </Routes>
        </Router>
    );
}

export default App;