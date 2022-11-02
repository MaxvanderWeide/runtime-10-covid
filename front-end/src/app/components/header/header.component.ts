import {Component, ElementRef, OnInit} from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

  constructor(private eRef: ElementRef) {
    if (localStorage.getItem('theme') === 'theme-dark') {
      document.body.classList.add('theme-dark');
    } else {
      localStorage.setItem('theme', 'theme-light');
    }
  }

  public toggleThemeMode(): void {
    if (localStorage.getItem('theme') === 'theme-light') {
      document.body.classList.add('theme-dark');
      localStorage.setItem('theme', 'theme-dark');
    } else if (localStorage.getItem('theme') === 'theme-dark') {
      document.body.classList.remove('theme-dark');
      localStorage.setItem('theme', 'theme-light');
    } else {
      localStorage.setItem('theme', 'theme-light');
    }
  }

  ngOnInit(): void {
  }

}
