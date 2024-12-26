//import "./App.css";
import Menu from "./components/Menu.tsx";
import './App.css';
import axios from "axios";
import {useEffect} from "react";
function App() {

        const fetchAPI = async () => {
            const response = await axios.get("http://localhost:3001/results");
            console.log(response.data);
        }
        useEffect(() => {
            fetchAPI();
        }, []);

        return (
            <div>
                <Menu/>

            </div>
        );
}

export default App;
