import { Component, OnInit, HostListener } from '@angular/core';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-about-us',
  templateUrl: './about-us.component.html',
  styleUrls: ['./about-us.component.scss']
})
export class AboutUsComponent implements OnInit {

  arrowsOutside = true;

  partners = [
    {
      type: 'partner',
      path: 'assets/images/partners/city.png',
      name: 'City of Toronto',
    },
    {
      type: 'partner',
      path: 'assets/images/partners/utsc.png',
      name: 'University of Toronto Scarborough',
    },
    {
      type: 'partner',
      path: 'assets/images/partners/centennial.png',
      name: 'Centennial College',
    },
  ];

  constructor(
    private titleService: Title,
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle("About Us | Find Dining Scarborough");
  }

  @HostListener('window:resize', ['$event'])
  onResize() {
    this.arrowsOutside = window.innerWidth < 800 ? false : true;
  }

}
