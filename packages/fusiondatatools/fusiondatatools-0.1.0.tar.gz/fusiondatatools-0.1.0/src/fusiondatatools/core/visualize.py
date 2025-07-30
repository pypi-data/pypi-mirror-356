import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def closest_factors(N):
    # the largest dimension we need to consider is up to ceil(sqrt(N))
    max_side = np.ceil(np.sqrt(N))
    
    best = (1, N)           # fallback: 1×N
    best_diff = np.abs(N - 1)
    
    for r in np.arange(1, max_side + 1):
        # smallest c so that r*c >= N
        c = np.ceil(N / r)
        diff = np.abs(c - r)
        # pick the pair with the smallest |c-r|
        if diff < best_diff:
            best = (r, c)
            best_diff = diff
    best = (int(best[0]), int(best[1]))
    return best

def imshow(x, channel=0, labels=None, title=None, orientation='horizontal', rgb=False):
    
    if orientation == 'horizontal':
        shape = (1, 2)
        figsize = (12, 4)
    elif orientation == 'vertical':
        shape = (2, 1)
        figsize = (4, 4)
    else:
        raise ValueError("Invalid orientation. Must be 'horizontal' or 'vertical'.")
        
    if isinstance(x, tuple):
        feature, label = x
        fig, axs = plt.subplots(shape[0], shape[1], figsize=figsize)
        if rgb:
            feature = feature.numpy()
            inputs_vis = (feature - np.min(feature, axis=(1, 2), keepdims=True)) / (np.max(feature, axis=(1, 2), keepdims=True) - np.min(feature, axis=(1, 2), keepdims=True))
            inputs_vis = inputs_vis.transpose(1, 2, 0)
            axs[0].imshow(inputs_vis, aspect='auto', origin='lower', cmap='gist_heat')
        else:
            axs[0].imshow(feature[channel], aspect='auto', origin='lower', cmap='gist_heat')
        axs[0].set_title('Feature')
        axs[1].imshow(label, aspect='auto', origin='lower', interpolation='none')
        if labels is not None:
            axs[1].set_yticks(range(len(labels)))
            axs[1].set_yticklabels(labels)
        axs[1].set_title('Label')
        if title is not None:
            fig.suptitle(title)
        plt.tight_layout()
        plt.show()
    else:
        plt.figure(figsize=(6, 4))
        if rgb:
            feature = x.numpy()
            inputs_vis = (feature - np.min(feature, axis=(1, 2), keepdims=True)) / (np.max(feature, axis=(1, 2), keepdims=True) - np.min(feature, axis=(1, 2), keepdims=True))
            inputs_vis = inputs_vis.transpose(1, 2, 0)
            plt.imshow(inputs_vis, aspect='auto', origin='lower', cmap='gist_heat')
        else:
            plt.imshow(x[channel], aspect='auto', origin='lower', interpolation='none', cmap='gist_heat')
        plt.title('Feature')
        
def imshow_super(x, channels, labels=None, title=None):
    
    rows, cols = closest_factors(x.shape[0])
    
    if rows == 1:
        fig, ax = plt.subplots(1, len(x), figsize=(3*len(x), 3), dpi=300)
        for i, channel in enumerate(x):
            ax[i].imshow(
                channel, 
                aspect='auto', origin='lower', cmap='gist_heat')
            ax[i].set_title(f'{channels[i]}')
            ax[i].axis('off')
            
    else:
        fig, ax = plt.subplots(
            rows, cols, 
            figsize=(3*cols, 3*rows), dpi=300)
        row, col = 0, 0
        for i, channel in enumerate(x):
            ax[row, col].imshow(
                channel, 
                aspect='auto', origin='lower', cmap='gist_heat')
            ax[row, col].set_title(f'{channels[i]}')
            row += 1
            if row == rows:
                row = 0
                col += 1
        for row in range(rows):
            for col in range(cols):
                    ax[row, col].axis('off')
    
    if title is not None: fig.suptitle(title)
    plt.tight_layout()
    return fig

def superplot(features, labels, diagnostics, label_names, shot_number, time_range, fs_range, plot_idx=0):
    """
    Generates and saves a plot comparing feature spectrograms and labels.

    Args:
        features (list): List of 2D numpy arrays representing spectrograms for each diagnostic.
        labels (np.ndarray): 2D numpy array of labels over time.
        diagnostics (list): List of names for each diagnostic/feature.
        label_names (list): List of names for each label category.
        shot_number (int): Identifier for the data shot.
        time_range (tuple): Start and end time as numpy datetime64 objects.
        fs_range (np.ndarray): Array of frequency values (assumed in kHz).
        plot_idx (int): Index for naming the output plot file.
    """
    num_channels = len(diagnostics)
    plot_rows, plot_cols = closest_factors(num_channels)
    num_labels = len(label_names)

    # Ensure labels is 2D
    labels = labels.squeeze()

    # Convert time range to milliseconds
    time_start_ms, time_end_ms = (t.astype('timedelta64[ns]').astype(float) / 1e6 for t in time_range)
    time_extent_ms = [time_start_ms, time_end_ms]

    # Get frequency range limits (assuming fs_range is already in kHz)
    freq_min_khz, freq_max_khz = fs_range[0], fs_range[-1]
    freq_extent_khz = [freq_min_khz, freq_max_khz]

    fig = plt.figure(figsize=(10, 7), dpi=300)
    # Main grid: 1 row, 2 columns (features left, labels right)
    gs_main = gridspec.GridSpec(1, 2, width_ratios=[2, 1], figure=fig)
    # Grid for feature channels within the left part of the main grid
    gs_channels = gridspec.GridSpecFromSubplotSpec(
        plot_rows, plot_cols, subplot_spec=gs_main[0], hspace=0.3, wspace=0.3)

    axes_list = [] # To store axes for sharing properties
    for idx, diag_name in enumerate(diagnostics):
        row = idx // plot_cols
        col = idx % plot_cols

        # Share x and y axes with the first plot (axes_list[0])
        share_ax = axes_list[0] if idx > 0 else None
        ax = fig.add_subplot(gs_channels[row, col], sharex=share_ax, sharey=share_ax)
        axes_list.append(ax)

        # Set axis labels only on the outer plots
        if col == 0:  # Leftmost column
            ax.set_ylabel('Frequency [kHz]')
        if row == plot_rows - 1:  # Bottom row
            ax.set_xlabel('Time [ms]')

        # Plot the power spectral density (feature)
        power_spectral_density = features[idx]
        im = ax.imshow(
            power_spectral_density,
            origin='lower',
            aspect='auto',
            cmap='gist_heat',
            interpolation='nearest',
            extent=time_extent_ms + freq_extent_khz, # [left, right, bottom, top]
        )
        ax.set_title(diag_name)

        # Hide tick labels for inner plots automatically due to sharing axes
        # (No explicit hiding needed if sharex/sharey works as expected)

    # Labels subplot (right part of the main grid)
    ax_labels = fig.add_subplot(gs_main[1])
    im_labels = ax_labels.imshow(
        labels,
        origin='lower',
        aspect='auto',
        interpolation='nearest',
        extent=time_extent_ms + [0, num_labels], # Time extent and label index extent
    )
    ax_labels.set_yticks(np.arange(num_labels) + 0.5) # Center ticks on label rows
    ax_labels.set_yticklabels(label_names, rotation=45, ha='right')
    ax_labels.set_xlabel('Time [ms]')
    ax_labels.set_title('Labels')

    # Add horizontal lines separating label categories
    for i in range(1, num_labels):
        ax_labels.axhline(i, color='white', linestyle='--', linewidth=0.5)

    plt.suptitle(f"Shot {shot_number}", fontsize=16)
    # Adjust layout to prevent overlap, especially with suptitle
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.savefig(f"{plot_idx}.png", dpi=300, bbox_inches='tight')
    plt.close(fig) # Close the figure to free up memory