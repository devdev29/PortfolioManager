import { Component } from '@angular/core';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})

export class LoginComponent {
    public username: string = '';
    public password: string = '';

    onSubmit() {
        // Implement your login logic here
        console.log('Username:', this.username);
        console.log('Password:', this.password);
        // Add authentication logic and navigate to the next page upon successful login
    }

//     var login = document.getElementById('login');
// var register = document.getElementById('register');
// var btn = document.getElementById('btn');

// function registered() {
//     login.style.left = "-400px";
//     register.style.left = "50px";
//     btn.style.left = "110px";
// }

// function logined() {
//     login.style.left = "50px";
//     register.style.left = "450px";
//     btn.style.left = "0";
// }
}