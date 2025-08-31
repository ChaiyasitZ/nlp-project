# MongoDB Atlas Setup Instructions

## 1. Create Database User
1. Go to MongoDB Atlas → Database Access
2. Click "+ ADD NEW DATABASE USER"
3. Set authentication method to "Password"
4. Choose a username and password
5. Set privileges to "Read and write to any database"
6. Click "Add User"

## 2. Configure Network Access
1. Go to MongoDB Atlas → Network Access
2. Click "+ ADD IP ADDRESS"
3. For development, add "0.0.0.0/0" (allows from anywhere)
4. Or add your specific IP address
5. Click "Confirm"

## 3. Get Connection String
1. Go to MongoDB Atlas → Database → Connect
2. Choose "Connect your application"
3. Select "Python" and version "3.6 or later"
4. Copy the connection string
5. Replace <password> with your actual password

## 4. Update .env File
Replace the MONGO_URI in your .env file with the correct connection string:

MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/newstimelineai?retryWrites=true&w=majority

Example:
MONGO_URI=mongodb+srv://myuser:mypassword@cluster0.abc123.mongodb.net/newstimelineai?retryWrites=true&w=majority

## 5. Test Connection
Run: python test_mongodb_connection.py

## Common Issues:
- Authentication failed → Check username/password
- Network timeout → Check network access settings
- Cluster paused → Resume cluster in Atlas dashboard
