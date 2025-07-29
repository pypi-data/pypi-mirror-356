import React from "react";
import PropTypes from "prop-types";

import { Button } from "semantic-ui-react";

import { i18next } from "@translations/i18next";

const ClipboardCopyButton = ({ copyText }) => {
  return (
    <Button
      icon="copy outline"
      title={`${i18next.t("Click to copy")}: ${copyText}`}
      link
      color="transparent"
      className="copy-button rel-ml-1"
      data-clipboard-text={copyText}
    />
  );
};

ClipboardCopyButton.propTypes = {
  copyText: PropTypes.string.isRequired,
};

export default ClipboardCopyButton;
