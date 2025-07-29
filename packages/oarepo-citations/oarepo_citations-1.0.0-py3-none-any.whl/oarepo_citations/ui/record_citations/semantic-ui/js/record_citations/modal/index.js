import React from "react";
import ReactDOM from "react-dom";

import { RecordCitationsModal } from "./components";

const recordCitationAppDiv = document.getElementById("record-citations");

ReactDOM.render(
  <RecordCitationsModal
    record={JSON.parse(recordCitationAppDiv.dataset.record)}
  />,
  recordCitationAppDiv
);

export { RecordCitationsModal };