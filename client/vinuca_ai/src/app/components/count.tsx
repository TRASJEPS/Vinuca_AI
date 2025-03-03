'use client'
import { useState } from "react";

const vinucaButton = 
{
    margin: "5px",
    marginTop: "15px",
    marginLeft: "20px",
    marginRight: "20px",
    paddingTop: "10px",
    paddingBottom: "10px",
    paddingLeft: "20px",
    paddingRight: "20px",
    background: "rgb(255, 148, 203)",
    color: "white",
    fontWeight: "bolder",
    fontSize: "large",
    border: "none",
    borderRadius: "15px",
};

export const Count = () => {
    console.log("Count Button");

    const [count, setCount] = useState(0);
    return (
        <button style={vinucaButton} onClick={() => setCount(count + 1)}>Clicked {count} times</button>
    )
}