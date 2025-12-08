// backend/routes/orderRoutes.js
import { Router } from 'express';
import Order from '../models/Order.js';
import Product from '../models/Product.js';
import jwt from 'jsonwebtoken';

const router = Router();
const JWT_SECRET = process.env.JWT_SECRET; 

// --- Helper Middleware (Assumed to be defined/imported) ---
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

// =========================================================
// 1. POST: Place New Order (Buyer Only)
router.post('/', verifyToken, async (req, res) => {
    if (req.user.role !== 'Buyer') {
        return res.status(403).json('Only buyers can place orders.');
    }
    
    try {
        const { items, shippingAddress, paymentMethod } = req.body;
        let totalAmount = 0;
        const orderItems = [];
        
        // 1. Validate items, calculate total, and check/reduce stock
        for (const item of items) {
            const product = await Product.findById(item.productId);

            if (!product || product.quantity < item.quantity) {
                return res.status(400).json({ message: `Insufficient stock for product ID: ${item.productId}` });
            }
            
            totalAmount += product.price * item.quantity;
            
            orderItems.push({
                productId: item.productId,
                name: product.name,
                quantity: item.quantity,
                price: product.price,
                farmerId: product.farmerId 
            });

            // Reduce stock
            product.quantity -= item.quantity;
            await product.save();
        }

        // 2. Create Order
        const newOrder = new Order({
            buyerId: req.user.id,
            items: orderItems,
            totalAmount,
            shippingAddress,
            paymentMethod
        });

        const savedOrder = await newOrder.save();
        res.status(201).json(savedOrder);
    } catch (err) {
        res.status(500).json({ message: 'Error placing order', error: err.message });
    }
});

// 2. GET: View Buyer's Order History
router.get('/history', verifyToken, async (req, res) => {
    try {
        const orders = await Order.find({ buyerId: req.user.id }).sort({ createdAt: -1 });
        res.status(200).json(orders);
    } catch (err) {
        res.status(500).json({ message: 'Failed to fetch order history' });
    }
});

// 3. GET: View Farmer's Incoming Orders (To be refined with aggregation later)
// (This route is complex, focusing on finding orders where ANY item belongs to the farmer)
router.get('/farmer-orders', verifyToken, async (req, res) => {
    if (req.user.role !== 'Farmer') {
        return res.status(403).json('Access denied.');
    }
    try {
        // Find orders where the authenticated farmerId matches the farmerId in any item
        const orders = await Order.find({ "items.farmerId": req.user.id }).sort({ createdAt: -1 });
        res.status(200).json(orders);
    } catch (err) {
        res.status(500).json({ message: 'Failed to fetch farmer orders' });
    }
});


export default router;