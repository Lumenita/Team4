import React, {useState, useEffect} from 'react'
import "./Style.css"

function MenuItem(props) {
    return(
        <li className = "MenuItem">
            <p>
               {props.button}
            </p>
        </li>
    );

}

function Menu(props) {
    return(
    <nav className = "menu">
        <ul className = "menu-nav">         
            {props.children} 
        </ul>
    </nav>
    );
}
export default Menu