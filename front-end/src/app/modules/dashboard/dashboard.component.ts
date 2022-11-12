import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  public multi = [
    {
      name: 'Progression',
      series: [
        {
          name: new Date('2021-09-01'),
          value: 12
        },
        {
          name: new Date('2021-10-01'),
          value: 15
        },
        {
          name: new Date('2021-11-01'),
          value: 18
        },
        {
          name: new Date('2021-12-01'),
          value: 28
        }
      ]
    },

    {
      name: 'Expected',
      series: [
        {
          name: new Date('2021-12-01'),
          value: 28
        },
        {
          name: new Date('2022-01-01'),
          value: 49
        }
      ]
    }
  ];

  constructor() { }

  ngOnInit(): void {
  }

}
