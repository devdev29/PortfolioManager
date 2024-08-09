import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent { 
    title = 'Croissant Dashboard';
    public domain = 'http://localhost:5000/';
}
