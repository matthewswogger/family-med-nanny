# Medication Management SMS API

A FastAPI backend service that allows users to manage their medications via SMS using Twilio. Users can add medications, log when they take them, and view their medication history through simple text messages.

## Features

- 📱 **SMS Integration**: Manage medications through text messages
- 💊 **Medication Tracking**: Add, log, and track medications
- 📅 **Daily Logs**: View today's medication history
- 🤖 **Natural Language**: Understand both structured commands and natural language
- 🔍 **Debug Endpoints**: API endpoints to view data for debugging

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Twilio Account

1. Go to [Twilio Console](https://console.twilio.com/)
2. Sign up for a free account
3. Get a phone number for SMS
4. Note your Account SID and Auth Token

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example file
cp env_example.txt .env
```

Edit `.env` with your Twilio credentials:

```env
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
```

### 4. Run the Application

```bash
# Development
python app.py

# Or using uvicorn directly
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 5. Configure Twilio Webhook

1. Go to your Twilio phone number settings
2. Set the webhook URL for incoming messages to:
   ```
   https://your-domain.com/webhook/sms
   ```
3. Make sure your server is publicly accessible (use ngrok for local development)

## Usage Examples

### Adding Medications

```
ADD aspirin 81mg daily
ADD metformin 500mg twice daily
ADD blood pressure med 10mg morning
```

### Logging Medications Taken

```
TAKE aspirin
I took my metformin
Just took blood pressure med
```

### Viewing Information

```
LIST          # Show all medications
TODAY         # Show today's taken medications
HELP          # Show available commands
```

## API Endpoints

### SMS Webhook
- **POST** `/webhook/sms` - Handles incoming SMS messages from Twilio

### Debug Endpoints
- **GET** `/` - Health check
- **GET** `/medications/{phone_number}` - Get medications for a phone number
- **GET** `/logs/{phone_number}` - Get medication logs for a phone number

## Local Development with ngrok

For local development, use ngrok to expose your local server:

```bash
# Install ngrok
# Download from https://ngrok.com/

# Start your FastAPI server
python app.py

# In another terminal, expose your local server
ngrok http 8000

# Use the ngrok URL as your Twilio webhook
# Example: https://abc123.ngrok.io/webhook/sms
```

## Message Parsing

The system understands both structured commands and natural language:

### Structured Commands
- `ADD [medication] [dosage] [frequency]`
- `TAKE [medication]`
- `LIST`
- `TODAY`
- `HELP`

### Natural Language
- "I took my aspirin"
- "Just took blood pressure medication"
- "Took metformin"

## Data Storage

Currently uses in-memory storage. For production, consider:

1. **SQLite**: Simple file-based database
2. **PostgreSQL**: Robust relational database
3. **MongoDB**: Document-based storage

## Security Considerations

- Validate phone numbers
- Implement rate limiting
- Add authentication for admin endpoints
- Encrypt sensitive health data
- Follow HIPAA guidelines if applicable

## Production Deployment

### Using Heroku

1. Create a Heroku app
2. Set environment variables in Heroku dashboard
3. Deploy using Git

```bash
heroku create your-app-name
heroku config:set TWILIO_ACCOUNT_SID=your_sid
heroku config:set TWILIO_AUTH_TOKEN=your_token
heroku config:set TWILIO_PHONE_NUMBER=your_number
git push heroku main
```

### Using Railway

1. Connect your GitHub repository
2. Set environment variables
3. Deploy automatically

## Testing

Test the API locally:

```bash
# Test health endpoint
curl http://localhost:8000/

# Test medication endpoint (replace with actual phone number)
curl http://localhost:8000/medications/+1234567890
```

## Future Enhancements

- [ ] Database integration (SQLAlchemy)
- [ ] User authentication
- [ ] Medication reminders
- [ ] Drug interaction warnings
- [ ] Family member access
- [ ] Export functionality
- [ ] Photo logging
- [ ] Integration with health apps

## Troubleshooting

### Common Issues

1. **Webhook not receiving messages**: Check if your server is publicly accessible
2. **Environment variables not loading**: Make sure `.env` file is in the project root
3. **Twilio authentication errors**: Verify your Account SID and Auth Token
4. **Port already in use**: Change the port in `app.py` or kill the process using the port

### Logs

The application logs all incoming messages and responses. Check the console output for debugging information.

## License

MIT License - feel free to use this for your medication management needs! 