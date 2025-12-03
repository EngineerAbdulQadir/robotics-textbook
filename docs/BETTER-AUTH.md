To Run Docker:

1. Open a new terminal
2. Run 'docker start postgres_auth'


To Run Auth Backend:

1. Open a new terminal
2. Navigate to the auth-backend directory
3. Run `npm run dev`

To Run Test Client:

1. Open a new terminal
2. Navigate to the auth-backend directory
3. Run `npx http-server -p 8080 --cors`

Populate the .env file with the following:
$env:DATABASE_URL="postgresql://authuser:authpass123@localhost:5432/auth"
$env:BETTER_AUTH_SECRET="eff354f994fc9b2441880533bdd89936860480e13715b5eccaad61fc57c9ee2a"