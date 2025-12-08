import mongoose from 'mongoose';

const OrderItemSchema = new mongoose.Schema({
    productId: { type: mongoose.Schema.Types.ObjectId, ref: 'Product', required: true },
    name: { type: String, required: true },
    quantity: { type: Number, required: true, min: 1 },
    price: { type: Number, required: true },
    farmerId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true }
});

const OrderSchema = new mongoose.Schema({
    buyerId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    items: [OrderItemSchema],
    status: { 
        type: String, 
        enum: ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled'],
        default: 'Pending'
    },
    totalAmount: { type: Number, required: true },
    shippingAddress: { type: String, required: true },
    paymentMethod: { type: String, default: 'Cash on Delivery' }
}, { timestamps: true });

export default mongoose.model('Order', OrderSchema);