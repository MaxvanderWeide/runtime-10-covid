import {AfterViewInit, Component, OnInit} from '@angular/core';
import {DataService} from "../../services/data.service";

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  public multi = [];

  constructor(private dataService: DataService) { }

  ngOnInit(): void {
    this.dataService.getCases().subscribe(response => {
      this.multi = response;
      console.log(this.multi);
    })
  }

}
