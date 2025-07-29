# OARepo Citations

A citation management extension for OARepo that provides comprehensive citation functionality for academic records. This package enables users to generate and export citations in multiple academic formats directly from record detail pages.

## Installation

Install the package using pip:

```bash
pip install oarepo-citations
```

## Usage

### Basic Integration

Once installed, the citation functionality is automatically available on record detail pages. The package provides:

1. **Citation Dropdown Component**: A compact dropdown selector for citation styles
2. **Citation Modal Component**: An expanded modal view for detailed citation information

### Template Integration

Include citations in your record templates:

```jinja
{% include 'RecordCitations.jinja' %}
```

### JavaScript Components

The package exports React components that can be used in custom implementations:

```javascript
import { RecordCitationsDropdown, RecordCitationsModal } from '@js/record_citations';
```

## License

This project is part of the OARepo ecosystem developed by CESNET.

## Support

For issues and questions, please use the project's issue tracker or contact the development team at CESNET.

