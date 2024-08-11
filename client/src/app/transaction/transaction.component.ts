import { HttpClient } from '@angular/common/http';
import { Component, OnInit, AfterViewInit, Injectable } from '@angular/core';
import { faArrowTrendDown, faArrowTrendUp, faNewspaper } from '@fortawesome/free-solid-svg-icons';
import { Chart, registerables } from 'chart.js';
import { catchError, Observable, throwError } from 'rxjs';
import { AppComponent } from '../app.component';

@Component ({
    selector : 'app-transaction',
    templateUrl : './transaction.component.html',
    styleUrls : ['./transaction.component.css']
})

@Injectable({
    providedIn: 'root'
})

export class TransactionComponent {}