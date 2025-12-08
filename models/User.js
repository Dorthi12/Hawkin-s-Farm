import mongoose from 'mongoose';

const UserSchema = new mongoose.Schema({
    username: { type: String, required: true, unique: true },
    password: { type: String, required: true },
    email: { type: String, required: true, unique: true },
    fullName: { type: String, required: true },
    phoneNumber: { type: String, required: true },
    role: { 
        type: String, 
        enum: ['Buyer', 'Farmer'], 
        required: true 
    },
    address: { type: String, required: true }
});

export default mongoose.model('User', UserSchema);