import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [products, setProducts] = useState([]);
  const [name, setName] = useState('');
  const [price, setPrice] = useState('');
  const [description, setDescription] = useState('');

  // Ürünleri API'den çekmek için useEffect kullan
  useEffect(() => {
    axios.get('http://localhost:5000/products')
      .then(response => {
        setProducts(response.data.data);
      })
      .catch(error => {
        console.error("There was an error fetching the products!", error);
      });
  }, []);

  // Yeni ürün ekleme fonksiyonu
  const addProduct = () => {
    axios.post('http://localhost:5000/products', { name, price, description })
      .then(() => {
        setName('');
        setPrice('');
        setDescription('');
        window.location.reload();
      });
  };

  return (
    <div>
      <h1>Product Management System</h1>
      <ul>
        {products.map(product => (
          <li key={product.id}>{product.name} - {product.price}</li>
        ))}
      </ul>
      <h2>Add a new product</h2>
      <input 
        type="text" 
        placeholder="Name" 
        value={name} 
        onChange={e => setName(e.target.value)} 
      />
      <input 
        type="text" 
        placeholder="Price" 
        value={price} 
        onChange={e => setPrice(e.target.value)} 
      />
      <input 
        type="text" 
        placeholder="Description" 
        value={description} 
        onChange={e => setDescription(e.target.value)} 
      />
      <button onClick={addProduct}>Add Product</button>
    </div>
  );
}

export default App;
