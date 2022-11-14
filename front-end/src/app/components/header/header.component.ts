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

      document.getElementById('dark-button').innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-sun" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">\n' +
          '   <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>\n' +
          '   <circle cx="12" cy="12" r="4"></circle>\n' +
          '   <path d="M3 12h1m8 -9v1m8 8h1m-9 8v1m-6.4 -15.4l.7 .7m12.1 -.7l-.7 .7m0 11.4l.7 .7m-12.1 -.7l-.7 .7"></path>\n' +
          '</svg>';

    } else if (localStorage.getItem('theme') === 'theme-dark') {
      document.body.classList.remove('theme-dark');
      localStorage.setItem('theme', 'theme-light');

      document.getElementById('dark-button').innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-moon-stars" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">\n' +
          '   <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>\n' +
          '   <path d="M12 3c.132 0 .263 0 .393 0a7.5 7.5 0 0 0 7.92 12.446a9 9 0 1 1 -8.313 -12.454z"></path>\n' +
          '   <path d="M17 4a2 2 0 0 0 2 2a2 2 0 0 0 -2 2a2 2 0 0 0 -2 -2a2 2 0 0 0 2 -2"></path>\n' +
          '   <path d="M19 11h2m-1 -1v2"></path>\n' +
          '</svg>';
    } else {
      localStorage.setItem('theme', 'theme-light');
      document.getElementById('dark-button').innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-moon-stars" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">\n' +
          '   <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>\n' +
          '   <path d="M12 3c.132 0 .263 0 .393 0a7.5 7.5 0 0 0 7.92 12.446a9 9 0 1 1 -8.313 -12.454z"></path>\n' +
          '   <path d="M17 4a2 2 0 0 0 2 2a2 2 0 0 0 -2 2a2 2 0 0 0 -2 -2a2 2 0 0 0 2 -2"></path>\n' +
          '   <path d="M19 11h2m-1 -1v2"></path>\n' +
          '</svg>';
    }
  }

  ngOnInit() {
  }
}
