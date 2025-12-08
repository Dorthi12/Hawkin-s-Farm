// backend/routes/productRoutes.js
import { Router } from 'express';
import Product from '../models/Product.js';
import jwt from 'jsonwebtoken';

const router = Router();
const JWT_SECRET = process.env.JWT_SECRET;

// --- Helper Middleware (You must implement this fully) ---
const verifyToken = (req, res, next) => {
    const authHeader = req.headers.authorization;
    if (authHeader) {
        const token = authHeader.split(' ')[1];
        jwt.verify(token, JWT_SECRET, (err, user) => {
            if (err) return res.status(403).json('Token is not valid!');
            req.user = user; // user = { id, role }
            next();
        });
    } else {
        res.status(401).json('You are not authenticated!');
    }
};

const isFarmer = (req, res, next) => {
    if (req.user.role !== 'Farmer') {
        return res.status(403).json('Access denied. Only Farmers can perform this action.');
    }
    next();
};

// =========================================================
// 1. GET: Get ALL products for the Marketplace (R - Read)
router.get('/', async (req, res) => {
    try {
        // Find products with stock greater than zero
        const products = await Product.find({ quantity: { $gt: 0 } }).sort({ createdAt: -1 }); 
        res.status(200).json(products);
    } catch (err) {
        res.status(500).json({ message: 'Failed to fetch products' });
    }
});

// 2. GET: Get a specific Farmer's listings (R - Read for Dashboard)
router.get('/my-listings', verifyToken, isFarmer, async (req, res) => {
    try {
        const products = await Product.find({ farmerId: req.user.id });
        res.status(200).json(products);
    } catch (err) {
        res.status(500).json({ message: 'Failed to fetch farmer listings' });
    }
});

// 3. POST: Create a new product (C - Create)
router.post('/', verifyToken, isFarmer, async (req, res) => {
    try {
        const newProduct = new Product({
            ...req.body,
            farmerId: req.user.id // Link product to the authenticated farmer
        });

        const savedProduct = await newProduct.save();
        res.status(201).json(savedProduct);
    } catch (err) {
        res.status(500).json({ message: 'Failed to create product', error: err.message });
    }
});

// 4. PUT: Update a specific product (U - Update)
router.put('/:id', verifyToken, isFarmer, async (req, res) => {
    try {
        // Ensure the farmer ID matches the product's farmerId for security
        const updatedProduct = await Product.findOneAndUpdate(
            { _id: req.params.id, farmerId: req.user.id }, 
            { $set: req.body },
            { new: true }
        );
        if (!updatedProduct) {
            return res.status(404).json('Product not found or unauthorized.');
        }
        res.status(200).json(updatedProduct);
    } catch (err) {
        res.status(500).json({ message: 'Error updating product' });
    }
});

// 5. DELETE: Delete a product listing (D - Delete)
router.delete('/:id', verifyToken, isFarmer, async (req, res) => {
    try {
        // Ensure the farmer ID matches the product's farmerId for security
        const deletedProduct = await Product.findOneAndDelete({ 
            _id: req.params.id, 
            farmerId: req.user.id 
        });
        if (!deletedProduct) {
            return res.status(404).json('Product not found or unauthorized.');
        }
        res.status(200).json('Product has been deleted.');
    } catch (err) {
        res.status(500).json({ message: 'Error deleting product' });
    }
});

export default router;