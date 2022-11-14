import {AfterViewInit, Component, OnInit} from '@angular/core';
import {DataService} from "../../services/data.service";

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  public cases = [];
  public deaths = [];
  public vaccin = [];

  constructor(private dataService: DataService) { }

  ngOnInit(): void {
    this.dataService.getCases().subscribe(response => {
      this.cases = response;
    })
    this.dataService.getDeaths().subscribe(response => {
      this.deaths = response;
    })
    this.dataService.getVaccin().subscribe(response => {
      this.vaccin = response;
    })
  }

}
