"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[8660],{19966:(e,t,o)=>{o.d(t,{A:()=>p});var l=o(96540),n=o(78518),i=o(19129),r=o(5261),s=o(73135),a=o(2445);const c={copyNode:(0,a.Y)("span",{children:(0,n.t)("Copy")}),onCopyEnd:()=>{},shouldShowText:!0,wrapped:!0,tooltipText:(0,n.t)("Copy to clipboard"),hideTooltip:!1};var d={name:"8irbms",styles:"display:inline-flex;align-items:center"};class u extends l.Component{constructor(e){super(e),this.copyToClipboard=this.copyToClipboard.bind(this),this.onClick=this.onClick.bind(this)}onClick(){this.props.getText?this.props.getText((e=>{this.copyToClipboard(Promise.resolve(e))})):this.copyToClipboard(Promise.resolve(this.props.text||""))}getDecoratedCopyNode(){return(0,l.cloneElement)(this.props.copyNode,{style:{cursor:"pointer"},onClick:this.onClick})}copyToClipboard(e){(0,s.A)((()=>e)).then((()=>{this.props.addSuccessToast((0,n.t)("Copied to clipboard!"))})).catch((()=>{this.props.addDangerToast((0,n.t)("Sorry, your browser does not support copying. Use Ctrl / Cmd + C!"))})).finally((()=>{this.props.onCopyEnd&&this.props.onCopyEnd()}))}renderTooltip(e){return(0,a.Y)(a.FK,{children:this.props.hideTooltip?this.getDecoratedCopyNode():(0,a.Y)(i.m_,{id:"copy-to-clipboard-tooltip",placement:"topRight",style:{cursor:e},title:this.props.tooltipText||"",trigger:["hover"],arrow:{pointAtCenter:!0},children:this.getDecoratedCopyNode()})})}renderNotWrapped(){return this.renderTooltip("pointer")}renderLink(){return(0,a.FD)("span",{css:d,children:[this.props.shouldShowText&&this.props.text&&(0,a.Y)("span",{className:"m-r-5","data-test":"short-url",children:this.props.text}),this.renderTooltip("pointer")]})}render(){const{wrapped:e}=this.props;return e?this.renderLink():this.renderNotWrapped()}}u.defaultProps=c;const p=(0,r.Ay)(u)},50068:(e,t,o)=>{o.d(t,{Dj:()=>s.Dj,cp:()=>s.cp,Ay:()=>r});var l=o(96453),n=o(2445);const i=l.I4.span`
  &,
  & svg {
    vertical-align: top;
  }
`;function r({checked:e=!1,onChange:t,style:o,className:l}){return(0,n.Y)(i,{style:o,onClick:()=>{t(!e)},role:"checkbox",tabIndex:0,"aria-checked":e,"aria-label":"Checkbox",className:l||"",children:e?(0,n.Y)(s.Dj,{}):(0,n.Y)(s.cp,{})})}var s=o(75264)},80037:(e,t,o)=>{o.d(t,{A:()=>V});var l=o(96540),n=o(96453);const i="NULL";var r=o(21013),s=o.n(r),a=o(31070),c=o(15311),d=o(46920),u=o(19966),p=o(18301),h=o(2445);function g(e){return"string"==typeof e&&/^"-?\d+"$/.test(e)?e.substring(1,e.length-1):e}function m(e){return(0,h.Y)(h.FK,{children:g(e)})}const C=({modalTitle:e,jsonObject:t,jsonValue:o})=>{const n=(0,c.B)(),i=(0,l.useMemo)((()=>"object"==typeof o?JSON.stringify(o):o),[o]);return(0,h.Y)(p.A,{modalBody:(0,h.Y)(a.d,{data:t,theme:n,valueRenderer:m}),modalFooter:(0,h.Y)(d.A,{children:(0,h.Y)(u.A,{shouldShowText:!1,text:i})}),modalTitle:e,triggerNode:(0,h.Y)(h.FK,{children:i})})};var b=o(78518),y=o(58642);var f=o(17437),v=o(66875),k=o(73135),x=o(49544);const S="-1";var w;!function(e){e.Small="small",e.Middle="middle"}(w||(w={}));var Y=o(67073),D=o(93103),A=o(6749);const N=n.I4.span`
  width: 14px;
`,F=({colId:e,api:t,pinnedLeft:o,pinnedRight:n,invisibleColumns:i,isMain:r,onVisibleChange:s})=>{var a;const c=(0,l.useCallback)((o=>{t.setColumnsPinned([e],o)}),[t,e]),d={label:(0,b.t)("Unhide"),key:"unHideSubMenu",icon:(0,h.Y)(Y.F.EyeInvisibleOutlined,{iconSize:"m"}),children:[i.length>1&&{key:"allHidden",label:(0,h.Y)("b",{children:(0,b.t)("All %s hidden columns",i.length)}),onClick:()=>{t.setColumnsVisible(i,!0)}},...i.map((e=>({key:e.getColId(),label:e.getColDef().headerName,onClick:()=>{t.setColumnsVisible([e.getColId()],!0)}})))].filter(Boolean)},u=[{key:"copyData",label:(0,b.t)("Copy the current data"),icon:(0,h.Y)(Y.F.CopyOutlined,{iconSize:"m"}),onClick:()=>{(0,k.A)((()=>new Promise(((o,l)=>{const n=t.getDataAsCsv({columnKeys:t.getAllDisplayedColumns().map((e=>e.getColId())).filter((t=>t!==e)),suppressQuotes:!0,columnSeparator:"\t"});n?o(n):l()}))))}},{key:"downloadCsv",label:(0,b.t)("Download to CSV"),icon:(0,h.Y)(Y.F.DownloadOutlined,{iconSize:"m"}),onClick:()=>{t.exportDataAsCsv({columnKeys:t.getAllDisplayedColumns().map((e=>e.getColId())).filter((t=>t!==e))})}},{type:"divider"},{key:"autoSizeAllColumns",label:(0,b.t)("Autosize all columns"),icon:(0,h.Y)(Y.F.ColumnWidthOutlined,{iconSize:"m"}),onClick:()=>{t.autoSizeAllColumns()}}];u.push(d),u.push({type:"divider"},{key:"resetColumns",label:(0,b.t)("Reset columns"),icon:(0,h.Y)(N,{className:"anticon"}),onClick:()=>{t.setColumnsVisible(i,!0);const e=t.getColumns();if(e){const o=e.filter((e=>e.getColId()!==S&&e.isPinned()));t.setColumnsPinned(o,null),t.moveColumns(e,0);const l=e.find((e=>e.getColId()!==S));l&&t.ensureColumnVisible(l,"start")}}});const p=[{key:"copy",label:(0,b.t)("Copy"),icon:(0,h.Y)(Y.F.CopyOutlined,{iconSize:"m"}),onClick:()=>{(0,k.A)((()=>new Promise(((o,l)=>{const n=t.getDataAsCsv({columnKeys:[e],suppressQuotes:!0});n?o(n):l()}))))}}];return(o||n)&&p.push({key:"unpin",label:(0,b.t)("Unpin"),icon:(0,h.Y)(Y.F.UnlockOutlined,{iconSize:"m"}),onClick:()=>c(null)}),o||p.push({key:"pinLeft",label:(0,b.t)("Pin Left"),icon:(0,h.Y)(Y.F.VerticalRightOutlined,{iconSize:"m"}),onClick:()=>c("left")}),n||p.push({key:"pinRight",label:(0,b.t)("Pin Right"),icon:(0,h.Y)(Y.F.VerticalLeftOutlined,{iconSize:"m"}),onClick:()=>c("right")}),p.push({type:"divider"},{key:"autosize",label:(0,b.t)("Autosize Column"),icon:(0,h.Y)(Y.F.ColumnWidthOutlined,{iconSize:"m"}),onClick:()=>{t.autoSizeColumns([e])}},{key:"hide",label:(0,b.t)("Hide Column"),icon:(0,h.Y)(Y.F.EyeInvisibleOutlined,{iconSize:"m"}),onClick:()=>{t.setColumnsVisible([e],!1)},disabled:(null==(a=t.getColumns())?void 0:a.length)===i.length+1}),i.length>0&&p.push(d),(0,h.Y)(D.LO,{placement:"bottomRight",trigger:["click"],onOpenChange:s,overlay:(0,h.Y)(A.W1,{style:{width:r?250:180},mode:"vertical",items:r?u:p})})},I=[null,"asc","desc"],z=n.I4.div`
  display: flex;
  flex: 1;
  &[role='button'] {
    cursor: pointer;
  }
`,T=n.I4.div`
  position: relative;
  display: inline-flex;
  align-items: center;
`,O=n.I4.span`
  position: absolute;
  right: 0;
`,L=n.I4.div`
  display: none;
  position: absolute;
  right: 0;
  &.main {
    flex-direction: row;
    justify-content: center;
    width: 100%;
  }
  & .antd5-dropdown-trigger {
    cursor: context-menu;
    padding: ${({theme:e})=>2*e.gridUnit}px;
    background-color: var(--ag-background-color);
    box-shadow: 0 0 2px var(--ag-chip-border-color);
    border-radius: 50%;
    &:hover {
      box-shadow: 0 0 4px ${({theme:e})=>e.colors.grayscale.light1};
    }
  }
`,M=n.I4.div`
  position: absolute;
  top: 0;
`,P={agColumnHeader:({enableFilterButton:e,enableSorting:t,displayName:o,setSort:i,column:r,api:s})=>{const a=(0,n.DP)(),c=r.getColId(),d=r.isPinnedLeft(),u=r.isPinnedRight(),p=(0,l.useRef)(0),[g,m]=(0,l.useState)([]),[C,y]=(0,l.useState)(null),[f,v]=(0,l.useState)(),k=(0,l.useCallback)((e=>{p.current=(p.current+1)%I.length;const t=I[p.current];i(t,e.shiftKey),y(t)}),[i]),x=(0,l.useCallback)((e=>{var t;e&&m((null==(t=s.getColumns())?void 0:t.filter((e=>!e.isVisible())))||[])}),[s]),w=(0,l.useCallback)((()=>{var e,t;const o=-1!==s.getAllDisplayedColumns().findIndex((e=>e.getSortIndex())),l=r.getSortIndex();p.current=I.indexOf(null!=(e=r.getSort())?e:null),y(null!=(t=r.getSort())?t:null),v(o?l:null)}),[s,r]);return(0,l.useEffect)((()=>(s.addEventListener("sortChanged",w),()=>{s.isDestroyed()||s.removeEventListener("sortChanged",w)})),[s,w]),(0,h.FD)(h.FK,{children:[c!==S&&(0,h.FD)(z,{tabIndex:0,className:"ag-header-cell-label",...t&&{role:"button",onClick:k,title:(0,b.t)("To enable multiple column sorting, hold down the ⇧ Shift key while clicking the column header.")},children:[(0,h.Y)("div",{className:"ag-header-cell-text",children:o}),t&&(0,h.FD)(T,{children:[(0,h.Y)(Y.F.Sort,{iconSize:"xxl"}),(0,h.FD)(M,{children:["asc"===C&&(0,h.Y)(Y.F.SortAsc,{iconSize:"xxl",iconColor:a.colors.primary.base}),"desc"===C&&(0,h.Y)(Y.F.SortDesc,{iconSize:"xxl",iconColor:a.colors.primary.base})]}),"number"==typeof f&&(0,h.Y)(O,{children:f+1})]})]}),e&&c&&s&&(0,h.Y)(L,{className:"customHeaderAction"+(c===S?" main":""),children:c&&(0,h.Y)(F,{colId:c,api:s,pinnedLeft:d,pinnedRight:u,invisibleColumns:g,isMain:c===S,onVisibleChange:x})})]})}},K=({api:e})=>e.refreshCells(),j=function({data:e,columns:t,sortable:o=!0,columnReorderable:i,height:r,externalFilter:s,showRowNumber:a,enableActions:c,size:d=w.Middle,striped:u}){const p=(0,n.DP)(),g=(0,l.useCallback)((()=>Boolean(s)),[s]),m=`${e.length}}`.length,C=(0,l.useCallback)((({event:e,column:t,data:o,value:l,api:n})=>{var i;if((null==document.getSelection||null==(i=document.getSelection())||null==i.toString||!i.toString())&&e&&"c"===e.key&&(e.ctrlKey||e.metaKey)){const e=t.getColId()===S?n.getAllDisplayedColumns().filter((e=>e.getColId()!==S)):[t],i=t.getColId()===S?[e.map((e=>e.getColId())).join("\t"),e.map((e=>null==o?void 0:o[e.getColId()])).join("\t")].join("\n"):String(l);(0,k.A)((()=>Promise.resolve(i)))}}),[]),b=(0,l.useMemo)((()=>[{field:S,valueGetter:"node.rowIndex+1",cellClass:"locked-col",width:30+6*m,suppressNavigable:!0,resizable:!1,pinned:"left",sortable:!1,...i&&{suppressMovable:!0}},...t.map((({label:e,headerName:l,width:n,render:i,comparator:r},s)=>({field:e,headerName:l,cellRenderer:i,sortable:o,comparator:r,...s===t.length-1&&{flex:1,width:n,minWidth:150}})))].slice(a?0:1)),[m,i,t,a,o]),y=(0,l.useMemo)((()=>({...!i&&{suppressMovable:!0},resizable:!0,sortable:o,filter:Boolean(c)})),[i,c,o]),Y=p.gridUnit*(d===w.Middle?9:7),D=(0,l.useMemo)((()=>({enableCellTextSelection:!0,ensureDomOrder:!0,suppressFieldDotNotation:!0,headerHeight:Y,rowSelection:"multiple",rowHeight:Y})),[Y]);return(0,h.FD)(x.A,{children:[(0,h.Y)(f.mL,{styles:()=>f.AH`
          #grid-table.ag-theme-quartz {
            --ag-icon-font-family: agGridMaterial;
            --ag-grid-size: ${p.gridUnit}px;
            --ag-font-size: ${p.typography.sizes[d===w.Middle?"m":"s"]}px;
            --ag-font-family: ${p.typography.families.sansSerif};
            --ag-row-height: ${Y}px;
            ${!u&&`--ag-odd-row-background-color: ${p.colors.grayscale.light5};`}
            --ag-border-color: ${p.colors.grayscale.light2};
            --ag-row-border-color: ${p.colors.grayscale.light2};
            --ag-header-background-color: ${p.colors.grayscale.light4};
          }
          #grid-table .ag-cell {
            -webkit-font-smoothing: antialiased;
          }
          .locked-col {
            background: var(--ag-row-border-color);
            padding: 0;
            text-align: center;
            font-size: calc(var(--ag-font-size) * 0.9);
            color: var(--ag-disabled-foreground-color);
          }
          .ag-row-hover .locked-col {
            background: var(--ag-row-hover-color);
          }
          .ag-header-cell {
            overflow: hidden;
          }
          & [role='columnheader']:hover .customHeaderAction {
            display: flex;
          }
        `}),(0,h.Y)("div",{id:"grid-table",className:"ag-theme-quartz",css:f.AH`
          width: 100%;
          height: ${r}px;
        `,children:(0,h.Y)(v.W6,{rowData:e,columnDefs:b,defaultColDef:y,onSortChanged:K,isExternalFilterPresent:g,doesExternalFilterPass:s,components:P,gridOptions:D,onCellKeyDown:C})})]})},R=/^(NaN|-?((\d*\.\d+|\d+)([Ee][+-]?\d+)?|Infinity))$/,$=n.I4.div`
  height: 100%;
  overflow: hidden;
`,E=e=>"string"==typeof e&&R.test(e)?parseFloat(e):e,H=(e,t)=>{const o=E(e),l=E(t);return o===l?0:null===o?1:null===l||o<l?-1:1},V=({orderedColumnKeys:e,data:t,height:o,filterText:n="",expandedColumns:r=[],allowHTML:a=!0,striped:c})=>{const d=function({columnKeys:e,expandedColumns:t}){const o=(0,l.useMemo)((()=>e.reduce(((e,o)=>({...e,[o]:null==t?void 0:t.some((e=>e.startsWith(`${o}.`)))})),{})),[t,e]);return(0,l.useCallback)((({cellData:e,columnKey:t})=>{if(null===e)return i;const l=String(e),n=l.substring(0,1);let r;return r="["===n?"[…]":"{"===n?"{…}":"",o[t]?r:l}),[o])}({columnKeys:e,expandedColumns:r}),u=(0,l.useMemo)((()=>e.map((e=>({key:e,label:e,fieldName:e,headerName:e,comparator:H,render:({value:e,colDef:t})=>(({cellData:e,getCellContent:t,columnKey:o,allowHTML:l=!0})=>{var n;const r=null!=(n=null==t?void 0:t({cellData:e,columnKey:o}))?n:String(e);if(null===e)return(0,h.Y)("i",{className:"text-muted",children:i});const a=function(e){if("object"==typeof e)return e;if("string"!=typeof e||-1===["{","["].indexOf(e.substring(0,1)))return null;try{const t=s()({storeAsString:!0}).parse(e);return t&&"object"==typeof t?t:null}catch(e){return null}}(e);return a?(0,h.Y)(C,{modalTitle:(0,b.t)("Cell content"),jsonObject:a,jsonValue:e}):l&&"string"==typeof e?(0,y.nn)(r):r})({cellData:e,columnKey:t.field,allowHTML:a,getCellContent:d})})))),[e,a,d]),p=(0,l.useRef)(n);p.current=n;const g=(0,l.useCallback)((e=>!p.current||!e.data||((e,t)=>{const o=[];Object.keys(t).forEach((e=>{if(t.hasOwnProperty(e)){const l=t[e];"string"==typeof l?o.push(l.toLowerCase()):null!==l&&"function"==typeof l.toString&&o.push(l.toString())}}));const l=e.toLowerCase();return o.some((e=>e.includes(l)))})(p.current,e.data)),[]);return(0,h.Y)($,{className:"filterable-table-container","data-test":"table-container",children:(0,h.Y)(j,{size:w.Small,height:o,usePagination:!1,columns:u,data:t,externalFilter:g,showRowNumber:!0,striped:c,enableActions:!0,columnReorderable:!0})})}}}]);