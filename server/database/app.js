const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const path = require('path');
const  cors = require('cors')
const app = express()
const port = 3030;

app.use(cors())
app.use(require('body-parser').urlencoded({ extended: false }));

const reviews_data = JSON.parse(fs.readFileSync(path.join(__dirname, "data/reviews.json"), 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync(path.join(__dirname, "data/dealerships.json"), 'utf8'));

mongoose.connect("mongodb://mongo_db:27017/",{'dbName':'dealershipsDB'}).catch(err => {
  console.log("MongoDB connection failed, running in mock mode");
});

const Reviews = require('./review');

const Dealerships = require('./dealership');

try {
  Reviews.deleteMany({}).then(()=>{
    Reviews.insertMany(reviews_data.reviews);
  }).catch(err => {
    console.log("deleteMany skipped - DB offline, using mock data");
  });
  Dealerships.deleteMany({}).then(()=>{
    Dealerships.insertMany(dealerships_data.dealerships);
  }).catch(err => {
    console.log("deleteMany skipped - DB offline, using mock data");
  });
  
} catch (error) {
  console.log("Error in data setup:", error.message);
}


// Express route to home
app.get('/', async (req, res) => {
    res.send("Welcome to the Mongoose API")
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    console.log("MongoDB error, returning mock reviews data");
    res.json(reviews_data.reviews);
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({dealership: parseInt(req.params.id)});
    res.json(documents);
  } catch (error) {
    console.log("MongoDB error, returning mock reviews data");
    const filtered = reviews_data.reviews.filter(r => r.dealership === parseInt(req.params.id));
    res.json(filtered);
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    const documents = await Dealerships.find();
    res.json(documents);
  } catch (error) {
    console.log("MongoDB error, returning mock data");
    res.json(dealerships_data.dealerships);
  }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const documents = await Dealerships.find({state: req.params.state});
    res.json(documents);
  } catch (error) {
    console.log("MongoDB error, returning mock data filtered by state");
    const filtered = dealerships_data.dealerships.filter(d => d.state === req.params.state);
    res.json(filtered);
  }
});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const documents = await Dealerships.find({id: parseInt(req.params.id)});
    res.json(documents);
  } catch (error) {
    console.log("MongoDB error, returning mock data for dealer ID");
    const filtered = dealerships_data.dealerships.filter(d => d.id === parseInt(req.params.id));
    res.json(filtered);
  }
});

//Express route to insert review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  data = JSON.parse(req.body);
  const documents = await Reviews.find().sort( { id: -1 } )
  let new_id = documents[0].id+1

  const review = new Reviews({
		"id": new_id,
		"name": data.name,
		"dealership": data.dealership,
		"review": data.review,
		"purchase": data.purchase,
		"purchase_date": data.purchase_date,
		"car_make": data.car_make,
		"car_model": data.car_model,
		"car_year": data.car_year,
	});

  try {
    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
		console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
