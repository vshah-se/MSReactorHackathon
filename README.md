# MSReactorHackathon
A day hackathon with Microsoft Reactor
 Hello World!

 Residential Landlord-Tenant Act: https://app.leg.wa.gov/rcw/default.aspx?cite=59.18


 Route:** `/chat`
 *   **Method:** `POST`
 *   **Expected Request Body (JSON):** `{ "query": "Your question here" }`
 *   **Response Body (JSON):** `{ "query": "Your question", "response": "The answer from the backend" }


#Docker Command for API
docker run -p 5000:5000 -v "$(pwd)/uploads:/app/uploads" msreactor-hackathon
