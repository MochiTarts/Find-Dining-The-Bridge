import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import {
  faCaretDown
} from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-filterlist-card',
  templateUrl: './filterlist-card.component.html',
  styleUrls: ['./filterlist-card.component.scss'],
})
export class FilterlistCardComponent implements OnInit {
  @Input() category: string;
  @Input() subcategories: string[];
  @Input() length: number;

  @Output() events: EventEmitter<any> = new EventEmitter<any>();

  checkMap: boolean[] = new Array(length);
  faCaretDown = faCaretDown;

  constructor() {}

  ngOnInit(): void {
    for (let i = 0; i < this.length; i++) {
      this.checkMap.push(false);
    }
  }

  /**
   * Emits the checkMap for favourites and all-restaurants page
   * to use for filtering
   */
  sendList() {
    this.events.emit(this.checkMap);
  }

  removeSpace(string) {
    return string.replace(/\s/g, "");
  }

  getSelecteds() {
    return this.checkMap.filter(Boolean).length;
  }

}
