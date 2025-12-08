
import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function Login({ onSuccessfulLogin }) {
    const [formData, setFormData] = useState({ username: '', password: '' });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.post('http://localhost:5000/api/auth/login', formData);

            
            localStorage.setItem('token', res.data.token);
            localStorage.setItem('userRole', res.data.role);

            // Redirect logic handled in App.js or similar
            onSuccessfulLogin(res.data.role); 
        } catch (error) {
            console.error('Login Error:', error.response?.data?.message);
            alert(error.response?.data?.message || 'Login failed. Check username and password.');
        }
    };

    return (
        <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
            {/* Auth Card (Dark/Minimalist Box) */}
            <div className="bg-gray-800 p-8 md:p-10 rounded-xl w-full max-w-md shadow-2xl border border-purple-800">
                
                <h2 className="text-3xl font-bold text-yellow-400 text-center mb-6">
                    Log In to Hawkins's Farm
                </h2>

                <form onSubmit={handleSubmit} className="space-y-4">
                    
                    {/* Username / Email */}
                    <div>
                        <label className="block text-sm font-medium text-gray-300">Username / Email</label>
                        <input type="text" name="username" value={formData.username} onChange={handleChange} placeholder="Your Username or Email" 
                            className="w-full mt-1 p-3 bg-gray-700 text-white border border-gray-600 rounded-md focus:ring-purple-500 focus:border-purple-500" required />
                    </div>

                    {/* Password */}
                    <div>
                        <label className="block text-sm font-medium text-gray-300">Password</label>
                        <input type="password" name="password" value={formData.password} onChange={handleChange} placeholder="Your Password" 
                            className="w-full mt-1 p-3 bg-gray-700 text-white border border-gray-600 rounded-md focus:ring-purple-500 focus:border-purple-500" required />
                    </div>

                    {/* Submit Button */}
                    <button type="submit" className="w-full py-3 mt-6 bg-yellow-500 text-black font-semibold rounded-md hover:bg-yellow-400 transition duration-150 shadow-lg">
                        Log In
                    </button>
                </form>

                <p className="mt-4 text-center text-gray-400 text-sm">
                    Need an account? <Link to="/signup" className="text-purple-400 hover:text-purple-300">Sign Up</Link>
                </p>
            </div>
        </div>
    );
}

export default Login;