import { Router } from 'express';
import User from '../models/User.js';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

const router = Router();
const JWT_SECRET = process.env.JWT_SECRET; // Ensure this is set in .env

// --- Register New User ---
router.post('/register', async (req, res) => {
    try {
        // Essential fields only
        const { username, email, password, role, address, fullName, phoneNumber } = req.body; 
        
        // 1. Validate input 
        if (!username || !password || !role || !fullName || !phoneNumber || !address) {
            return res.status(400).json({ message: 'Missing required fields' });
        }

        // 2. Hash Password
        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(password, salt);

        // 3. Create and save user
        const newUser = new User({ 
            username, 
            email, 
            password: hashedPassword, 
            role,
            address,
            fullName,
            phoneNumber
        });

        await newUser.save();
        res.status(201).json({ message: 'User registered successfully', user: newUser });
    } catch (err) {
        if (err.code === 11000) { 
            return res.status(409).json({ message: 'Username or email already exists' });
        }
        res.status(500).json({ message: 'Server error', error: err.message });
    }
});

// --- User Login ---
router.post('/login', async (req, res) => {
    try {
        const { username, password } = req.body;
        
       const user = await User.findOne({
    $or: [{ username }, { email: username }]
});
        // 1. Check if user exists  
        if (!user) {
            return res.status(401).json({ message: 'Invalid credentials' });
        }

        // 2. Check password
        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) { 
            return res.status(401).json({ message: 'Invalid credentials' }); 
        }

        // 3. Generate JWT Token
        const token = jwt.sign(
            { id: user._id, role: user.role }, 
            JWT_SECRET, 
            { expiresIn: '1d' }
        );

        res.status(200).json({ 
            token, 
            userId: user._id,
            role: user.role,
            message: 'Login successful' 
        });

    } catch (err) {
        res.status(500).json({ message: 'Server error', error: err.message });
    }
});

export default router;