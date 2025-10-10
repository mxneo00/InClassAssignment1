import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import axios from 'axios'

function App() {
  const [htmlContent, setHtmlContent] = useState(null)

  const [items, setItems] = useState([]);
  const [newItem, setNewItem] = useState("");

  const API_URL = "http://localhost:8000/items";

  useEffect(() => {
    fetch(API_URL).then((res) => res.json()).then(setItems).catch(console.error);
  })

  const addItem = async () => {
    if(!newItem.trim()) return;
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json"},
      body: JSON.stringify({ item_name: newItem }),
    });
    if (res.ok) {
      const item = await res.json();
      setItems((prev) => [...prev, item]);
      setNewItem("");
    }
  }

  const deleteItem = async (id) => {
    const res = await fetch(`${API_URL}/${id}`, {method: "DELETE"});
    if (res.ok) {
      setItems((prev) => prev.filter((item) => item.id !== id));
    }
  };

  return (
    <>
      <div>
        <h1>Item manager</h1>
        <input 
          value = {newItem}
          onChange={(e) => setNewItem(e.target.value)}
          placeholder="Enter item"
        />
        <button onClick={addItem}>Add item</button>

        <ul>
          {items.map((item) => (
            <li key={item.id}>
              {item.item_name} <button onClick={() => deleteItem(item.id)}>Delete</button>
            </li>
          ))}
        </ul>
      </div>
    </>
  )
}

export default App
