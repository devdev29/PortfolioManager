import { DatePipe } from "@angular/common";
import { Component } from "@angular/core";
import { faUser } from "@fortawesome/free-solid-svg-icons";

@Component ({
    selector : 'app-header',
    templateUrl : './header.component.html',
    styleUrls : ['./header.component.css'],
    providers: [DatePipe]
})

export class HeaderComponent {
    
    public currentDateTime: any;
    public faUser = faUser;
    public customer: string = "Isika Samanta";

    constructor(private datePipe: DatePipe) {}
    
    ngOnInit(): void {
        var curr = new Date();
        this.currentDateTime = this.datePipe.transform(curr, 'HH:mm\'hrs\' dd MMM yyyy');
        
    }
}