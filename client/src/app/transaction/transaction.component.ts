import { Component, Injectable } from '@angular/core';
import { catchError, Observable, throwError } from 'rxjs';
import { AppComponent } from '../app.component';
import { HttpClient } from '@angular/common/http';
import { DatePipe } from '@angular/common';

@Component ({
    selector : 'app-transaction',
    templateUrl : './transaction.component.html',
    styleUrls : ['./transaction.component.css']
})

@Injectable({
    providedIn: 'root'
})

export class TransactionComponent {
    public selectedDate = new Date(); 
    public transactionList: any = []; 

    constructor(private http: HttpClient, private app: AppComponent, private datePipe: DatePipe) { }

    errorHandler(error: {
        error: { message: string; };
        status: any; message: any;
    }) {
        let errorMessage = '';
        if (error.error instanceof ErrorEvent) {
            errorMessage = error.error.message;
        } 
        else {
            errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
        }
        return throwError(errorMessage);
    }

    getHistory(date: string): Observable<any> {
        return this.http.get(this.app.domain + 'transactions/history/' + date).pipe(catchError(this.errorHandler));
    }

    ngOnInit(): void {
        console.log('Today\'s Date:', this.selectedDate);
        const date = this.datePipe.transform(this.selectedDate, 'yyyy-MM-dd')
        console.log('Today\'s Date:', date);
        if(date == null)
            return;
        this.getHistory(date).subscribe(data => {
            console.log(data);
            this.transactionList = data;
        });
    }

    onDateChange() {
        console.log('Today\'s Date:', this.selectedDate);
        const date = this.datePipe.transform(this.selectedDate, 'yyyy-MM-dd');
        if(date == null)
            return;
        this.getHistory(date).subscribe(data => {
            console.log(data);
            this.transactionList = data;
        });
    }

}