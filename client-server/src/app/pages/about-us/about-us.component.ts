import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-about-us',
  templateUrl: './about-us.component.html',
  styleUrls: ['./about-us.component.scss']
})
export class AboutUsComponent implements OnInit {

  partners = [
    {
      path: 'assets/images/partners/city.png',
      name: 'City of Toronto',
      url: 'https://www.toronto.ca/',
    },
    {
      path: 'assets/images/partners/utsc.png',
      name: 'University of Toronto Scarborough',
      url: 'https://www.utsc.utoronto.ca/home/',
    },
    {
      path: 'assets/images/partners/centennial.png',
      name: 'Centennial College',
      url: 'https://www.centennialcollege.ca/',
    },
  ];

  constructor(
    private titleService: Title,
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle("About Us | Find Dining Scarborough");
  }
}
