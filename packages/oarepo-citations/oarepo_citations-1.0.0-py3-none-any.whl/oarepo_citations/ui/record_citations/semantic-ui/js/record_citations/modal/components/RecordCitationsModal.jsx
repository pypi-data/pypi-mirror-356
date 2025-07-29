import React, { useState, lazy, Suspense } from "react";
import PropTypes from "prop-types";

import { i18next } from "@translations/i18next";
import { Dimmer, Loader, Segment, Modal, Button } from "semantic-ui-react";

import TriggerButton from "./TriggerButton";

const CitationList = lazy(() => import("./CitationList"));

export const RecordCitationsModal = ({ record }) => {
  const [modalOpen, setModalOpen] = useState(false);

  return (
    <>
      <Modal
        onClose={() => setModalOpen(false)}
        onOpen={() => setModalOpen(true)}
        open={modalOpen}
        trigger={<TriggerButton />}
        role="dialog"
        aria-labelledby="citation-modal-header"
        aria-describedby="citation-modal-desc"
      >
        <Modal.Header as="h1" id="citation-modal-header">{i18next.t("Citations")}</Modal.Header>
        <Modal.Content>
          <p id="citation-modal-desc">{i18next.t("record-citation-modal-description")}</p>
          <Suspense
            fallback={
              <Dimmer.Dimmable as={Segment} placeholder dimmed role="presentation">
                <Dimmer simple inverted>
                  <Loader size="huge">{i18next.t("Loading")}…</Loader>
                </Dimmer>
              </Dimmer.Dimmable>
            }
          >
            <Segment>
              <CitationList record={record} />
            </Segment>
          </Suspense>
        </Modal.Content>
        <Modal.Actions>
          <Button title={i18next.t("Close citations modal window")} onClick={() => setModalOpen(false)}>
            {i18next.t("Close")}
          </Button>
        </Modal.Actions>
      </Modal>
    </>
  );
};

RecordCitationsModal.propTypes = {
  record: PropTypes.object.isRequired,
};
