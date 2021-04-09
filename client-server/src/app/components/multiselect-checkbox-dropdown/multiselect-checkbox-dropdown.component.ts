import { Component, OnInit, Input, Output, EventEmitter, OnChanges, SimpleChanges, ViewChild, ElementRef, AfterViewInit, HostListener } from '@angular/core';

@Component({
  selector: 'app-multiselect-checkbox-dropdown',
  templateUrl: './multiselect-checkbox-dropdown.component.html',
  styleUrls: ['./multiselect-checkbox-dropdown.component.scss']
})
export class MultiselectCheckboxDropdownComponent implements OnInit, OnChanges, AfterViewInit {
  @Input() list: any[] = [];
  @Input() initialCheckedList: any[] = [];

  @Output() shareCheckedList = new EventEmitter();

  initialList: any[] = [];
  checkedList: any[] = [];

  showDropDown = false;
  isFocused = false;

  containerWidth = 0;

  @ViewChild('dropdownContainer') dropdownContainer: ElementRef;

  constructor() { }

  ngOnInit(): void {
    for (let item of this.list) {
      this.initialList.push({name: item, checked: false});
    }
    this.checkedList = this.initialCheckedList;
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['initialCheckedList']) {
      this.checkedList = this.initialCheckedList;

      for (let i = 0; i < this.initialList.length; i++) {
        if (this.checkedList.includes(this.initialList[i].name)) {
          this.initialList[i].checked = true;
        } else {
          this.initialList[i].checked = false;
        }
      }
    }
  }

  ngAfterViewInit() {
    this.containerWidth = this.dropdownContainer.nativeElement.offsetWidth;
  }

  @HostListener('window:resize', ['$event'])
  onResize() {
    this.containerWidth = this.dropdownContainer.nativeElement.offsetWidth;
  }

  getSelectedValue(checked: Boolean, value:String){
    if (checked) {
      this.checkedList.push(value);
    } else {
      var index = this.checkedList.indexOf(value);
      this.checkedList.splice(index,1);
    }

    //share checked list
    this.shareCheckedlist();
  }

  shareCheckedlist(){
    this.shareCheckedList.emit(this.checkedList);
  }

  toggleDropdown(event) {
    if (this.isFocused) {
      this.showDropDown = !this.showDropDown;
    }
  }

}
