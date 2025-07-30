# MSI Viewer and Extractor

This interactive tool allows you to view the contents of MSI files and extract their files directly in your browser. The processing happens entirely on your device - no files are uploaded to any server.

Behind the scenes, it is running [pymsi](https://github.com/nightlark/pymsi/) using Pyodide.

<div id="msi-viewer-app">
  <div class="file-selector">
    <h2>Select an MSI File</h2>
    <input type="file" id="msi-file-input" accept=".msi" />
    <div id="loading-indicator" style="display: none;">Loading...</div>
  </div>

  <div id="msi-content" style="display: none;">
    <div class="tabs">
      <button class="tab-button active" data-tab="files">Files</button>
      <button class="tab-button" data-tab="tables">Tables</button>
      <button class="tab-button" data-tab="summary">Summary</button>
      <button class="tab-button" data-tab="streams">Streams</button>
    </div>
    <div class="tab-content">
      <div id="files-tab" class="tab-pane active">
        <h3>Files</h3>
        <button id="extract-button">Extract All Files (ZIP)</button>
        <div id="files-list-container">
          <table id="files-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Directory</th>
                <th>Size</th>
                <th>Component</th>
                <th>Version</th>
              </tr>
            </thead>
            <tbody id="files-list"></tbody>
          </table>
        </div>
      </div>
      <div id="tables-tab" class="tab-pane">
        <h3>Tables</h3>
        <select id="table-selector"></select>
        <div id="table-viewer-container">
          <table id="table-viewer">
            <thead id="table-header"></thead>
            <tbody id="table-content"></tbody>
          </table>
        </div>
      </div>
      <div id="summary-tab" class="tab-pane">
        <h3>Summary Information</h3>
        <div id="summary-content"></div>
      </div>
      <div id="streams-tab" class="tab-pane">
        <h3>Streams</h3>
        <div id="streams-content"></div>
      </div>
    </div>
  </div>
</div>

<style>
  #msi-viewer-app {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    max-width: 100%;
    margin: 0 auto;
  }

  .tabs {
    display: flex;
    margin-bottom: 1rem;
    border-bottom: 1px solid #ddd;
  }

  .tab-button {
    background: #f5f5f5;
    border: 1px solid #ddd;
    border-bottom: none;
    padding: 0.5rem 1rem;
    margin-right: 0.25rem;
    cursor: pointer;
  }

  .tab-button.active {
    background: white;
    border-bottom: 1px solid white;
    margin-bottom: -1px;
  }

  .tab-pane {
    display: none;
    padding: 1rem;
    border: 1px solid #ddd;
    border-top: none;
  }

  .tab-pane.active {
    display: block;
  }

  table {
    width: 100%;
    border-collapse: collapse;
  }

  th, td {
    text-align: left;
    padding: 0.5rem;
    border-bottom: 1px solid #ddd;
  }

  #extract-button {
    margin-bottom: 1rem;
    padding: 0.5rem 1rem;
    background: #4CAF50;
    color: white;
    border: none;
    cursor: pointer;
  }

  #files-list-container, #table-viewer-container {
    max-height: 500px;
    overflow-y: auto;
    border: 1px solid #ddd;
  }
</style>

<!-- Include the Pyodide script -->
<script type="text/javascript" src="https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.js"></script>

<!-- Include JSZip script -->
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>

<!-- Include the MSI viewer script with the correct path for ReadTheDocs -->
<script type="text/javascript" src="_static/msi_viewer.js"></script>
