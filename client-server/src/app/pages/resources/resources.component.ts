import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-resources',
  templateUrl: './resources.component.html',
  styleUrls: ['./resources.component.scss']
})
export class ResourcesComponent implements OnInit {

  constructor(
    private titleService: Title,
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle("Resources | Find Dining Scarborough");
  }

}
