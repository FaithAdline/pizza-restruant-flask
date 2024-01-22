// src/App.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';

const App = () => {
  const [restaurants, setRestaurants] = useState([]);
  const [pizzas, setPizzas] = useState([]);
  const [restaurantPizzas, setRestaurantPizzas] = useState([]);
  const [newRestaurantPizza, setNewRestaurantPizza] = useState({
    restaurant_id: 1, // replace with the actual default restaurant ID
    pizza_id: 1,      // replace with the actual default pizza ID
    price: 10,
  });

  // Fetch data on component mount
  useEffect(() => {
    fetchRestaurants();
    fetchPizzas();
    fetchRestaurantPizzas();
  }, []);

  const fetchRestaurants = async () => {
    try {
      const response = await axios.get('http://localhost:5000/restaurants');
      setRestaurants(response.data);
    } catch (error) {
      console.error('Error fetching restaurants:', error);
    }
  };

  const fetchPizzas = async () => {
    try {
      const response = await axios.get('http://localhost:5000/pizzas');
      setPizzas(response.data);
    } catch (error) {
      console.error('Error fetching pizzas:', error);
    }
  };

  const fetchRestaurantPizzas = async () => {
    try {
      const response = await axios.get('http://localhost:5000/restaurant_pizzas');
      setRestaurantPizzas(response.data);
    } catch (error) {
      console.error('Error fetching restaurant pizzas:', error);
    }
  };

  const handleCreateRestaurantPizza = async () => {
    try {
      await axios.post('http://localhost:5000/restaurant_pizzas', newRestaurantPizza);
      fetchRestaurantPizzas();
      // Optionally, you can reset the form or perform other actions after a successful creation
    } catch (error) {
      console.error('Error creating restaurant pizza:', error);
    }
  };

  return (
    <div>
      <h1>Pizza Restaurant App</h1>

      <h2>Restaurants</h2>
      <ul>
        {restaurants.map(restaurant => (
          <li key={restaurant.id}>{restaurant.name}</li>
        ))}
      </ul>

      <h2>Pizzas</h2>
      <ul>
        {pizzas.map(pizza => (
          <li key={pizza.id}>{pizza.name}</li>
        ))}
      </ul>

      <h2>Restaurant Pizzas</h2>
      <ul>
        {restaurantPizzas.map(restaurantPizza => (
          <li key={restaurantPizza.id}>
            {`Restaurant: ${restaurantPizza.restaurant.name}, Pizza: ${restaurantPizza.pizza.name}, Price: ${restaurantPizza.price}`}
          </li>
        ))}
      </ul>

      <h2>Create Restaurant Pizza</h2>
      <div>
        <label>Restaurant:</label>
        <select
          value={newRestaurantPizza.restaurant_id}
          onChange={(e) => setNewRestaurantPizza({ ...newRestaurantPizza, restaurant_id: e.target.value })}
        >
          {restaurants.map(restaurant => (
            <option key={restaurant.id} value={restaurant.id}>{restaurant.name}</option>
          ))}
        </select>

        <label>Pizza:</label>
        <select
          value={newRestaurantPizza.pizza_id}
          onChange={(e) => setNewRestaurantPizza({ ...newRestaurantPizza, pizza_id: e.target.value })}
        >
          {pizzas.map(pizza => (
            <option key={pizza.id} value={pizza.id}>{pizza.name}</option>
          ))}
        </select>

        <label>Price:</label>
        <input
          type="number"
          value={newRestaurantPizza.price}
          onChange={(e) => setNewRestaurantPizza({ ...newRestaurantPizza, price: e.target.value })}
        />

        <button onClick={handleCreateRestaurantPizza}>Create Restaurant Pizza</button>
      </div>
    </div>
  );
};

export default App;

