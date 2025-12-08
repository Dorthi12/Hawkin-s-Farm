import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import "../../index.css";


function Signup({ onSuccessfulSignup }) {
    const [formData, setFormData] = useState({
        fullName: '', username: '', email: '', password: '',
        phoneNumber: '', role: 'Buyer', address: ''
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.post('http://localhost:5000/api/auth/register', formData);

            alert(`Registration successful! Welcome, ${res.data.user.role}.`);
            onSuccessfulSignup();
        } catch (error) {
            console.error('Signup Error:', error.response?.data?.message);
            alert(error.response?.data?.message || 'Registration failed.');
        }
    };

    return (
        <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
            {/* Auth Card (Dark/Minimalist Box) */}
            <div className="bg-gray-800 p-8 md:p-10 rounded-xl w-full max-w-md shadow-2xl border border-purple-800">
                
                <h2 className="text-3xl font-bold text-yellow-400 text-center mb-6">
                    Sign Up for Hawkins's Farm
                </h2>

                <form onSubmit={handleSubmit} className="space-y-4">
                    
                    {/* Full Name */}
                    <div>
                        <label className="block text-sm font-medium text-gray-300">Full Name</label>
                        <input type="text" name="fullName" value={formData.fullName} onChange={handleChange} placeholder="Your Full Name" 
                            className="w-full mt-1 p-3 bg-gray-700 text-white border border-gray-600 rounded-md focus:ring-purple-500 focus:border-purple-500" required />
                    </div>

                    {/* Username */}
                    <div>
                        <label className="block text-sm font-medium text-gray-300">Username</label>
                        <input type="text" name="username" value={formData.username} onChange={handleChange} placeholder="Choose a Username" 
                            className="w-full mt-1 p-3 bg-gray-700 text-white border border-gray-600 rounded-md focus:ring-purple-500 focus:border-purple-500" required />
                    </div>
                    
                    {/* Email */}
                    <div>
                        <label className="block text-sm font-medium text-gray-300">Email</label>
                        <input type="email" name="email" value={formData.email} onChange={handleChange} placeholder="Your Email" 
                            className="w-full mt-1 p-3 bg-gray-700 text-white border border-gray-600 rounded-md focus:ring-purple-500 focus:border-purple-500" required />
                    </div>

                    {/* Password */}
                    <div>
                        <label className="block text-sm font-medium text-gray-300">Password</label>
                        <input type="password" name="password" value={formData.password} onChange={handleChange} placeholder="Your Password" 
                            className="w-full mt-1 p-3 bg-gray-700 text-white border border-gray-600 rounded-md focus:ring-purple-500 focus:border-purple-500" required />
                    </div>
                    
                    {/* Phone Number */}
                    <div>
                        <label className="block text-sm font-medium text-gray-300">Phone Number</label>
                        <input type="tel" name="phoneNumber" value={formData.phoneNumber} onChange={handleChange} placeholder="Your Phone Number" 
                            className="w-full mt-1 p-3 bg-gray-700 text-white border border-gray-600 rounded-md focus:ring-purple-500 focus:border-purple-500" required />
                    </div>

                    {/* Role Selection */}
                    <div>
                        <label className="block text-sm font-medium text-gray-300">Register as</label>
                        <select name="role" value={formData.role} onChange={handleChange} 
                            className="w-full mt-1 p-3 bg-gray-700 text-white border border-gray-600 rounded-md appearance-none focus:ring-purple-500 focus:border-purple-500" required>
                            <option value="Buyer">Buyer (Buy Produce)</option>
                            <option value="Farmer">Farmer (Sell Produce)</option>
                        </select>
                    </div>

                    {/* Address */}
                    <div>
                        <label className="block text-sm font-medium text-gray-300">Address</label>
                        <textarea name="address" value={formData.address} onChange={handleChange} placeholder="Shipping/Farm Address" 
                            className="w-full mt-1 p-3 bg-gray-700 text-white border border-gray-600 rounded-md focus:ring-purple-500 focus:border-purple-500" required />
                    </div>

                    {/* Submit Button */}
                    <button type="submit" className="w-full py-3 mt-6 bg-yellow-500 text-black font-semibold rounded-md hover:bg-yellow-400 transition duration-150 shadow-lg">
                        Submit
                    </button>
                </form>

                <p className="mt-4 text-center text-gray-400 text-sm">
                    Already have an account? <Link to="/login" className="text-purple-400 hover:text-purple-300">Log In</Link>
                </p>
            </div>
        </div>
    );
}

export default Signup;